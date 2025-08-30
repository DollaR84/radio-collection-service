import { useState, useEffect } from 'react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';
import { useBeforeUnload } from '../hooks/useBeforeUnload';
import { useTranslation } from 'react-i18next';

export default function ProfilePage() {
  const { token, logout } = useAuth();
  const { t } = useTranslation();
  const [initialData, setInitialData] = useState({
    user_name: '',
    email: '',
    first_name: '',
    last_name: '',
    access_rights: '',
    uuid_id: '',
    has_password: false
  });
  const [userData, setUserData] = useState({
    user_name: '',
    email: '',
    first_name: '',
    last_name: '',
    access_rights: '',
    uuid_id: ''
  });
  const [accessExpiresAt, setAccessExpiresAt] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [touched, setTouched] = useState(false);
  const [validationErrors, setValidationErrors] = useState({
    user_name: '',
    first_name: '',
    last_name: ''
  });
  
  // States for managing the password modal window
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false);
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [passwordErrors, setPasswordErrors] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  useBeforeUnload(touched, t("pages.profile.unsaved_changes"));

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get('/user/profile');
        const data = {
          user_name: response.data.user_name || '',
          email: response.data.email || '',
          first_name: response.data.first_name || '',
          last_name: response.data.last_name || '',
          access_rights: response.data.access_rights || 'default',
          uuid_id: response.data.uuid_id || '',
          has_password: response.data.has_password || false
        };
        setInitialData(data);
        setUserData(data);

        if (data.access_rights !== 'default' && data.access_rights !== 'owner' && data.uuid_id) {
          try {
            const rightsResp = await api.get(`/user/rights/${data.uuid_id}`);
            if (rightsResp.data.expires_at) {
              setAccessExpiresAt(rightsResp.data.expires_at);
            }
          } catch (err) {
            console.error("Failed to fetch access rights info:", err);
          }
        }
      } catch (error) {
        console.error('Failed to fetch user data:', error);
        setError(t("pages.profile.errors.fetch"));
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [token, t]);

  const hasChanges = () => {
    return (
      initialData.user_name !== userData.user_name ||
      initialData.first_name !== userData.first_name ||
      initialData.last_name !== userData.last_name
    );
  };

  const validate = () => {
    const errors = {
      user_name: '',
      first_name: '',
      last_name: ''
    };
    let isValid = true;

    if (!userData.user_name.trim()) {
      errors.user_name = t("pages.profile.errors.username_required");
      isValid = false;
    } else if (userData.user_name.length < 3) {
      errors.user_name = t("pages.profile.errors.username_short");
      isValid = false;
    }

    if (userData.user_name.length > 50) {
      errors.user_name = t("pages.profile.errors.user_name_long");
      isValid = false;
    }

    if (userData.first_name.length > 100) {
      errors.first_name = t("pages.profile.errors.first_name_long");
      isValid = false;
    }

    if (userData.last_name.length > 100) {
      errors.last_name = t("pages.profile.errors.last_name_long");
      isValid = false;
    }

    setValidationErrors(errors);
    return isValid;
  };

  // Password validation
  const validatePassword = () => {
    const errors = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    };
    let isValid = true;

    // If the user already has a password, the current password is required.
    if (initialData.has_password && !passwordData.current_password) {
      errors.current_password = t("pages.password.errors.current_password_required");
      isValid = false;
    }

    if (!passwordData.new_password) {
      errors.new_password = t("pages.password.errors.new_password_required");
      isValid = false;
    } else if (passwordData.new_password.length < 6) {
      errors.new_password = t("pages.password.errors.password_short");
      isValid = false;
    }

    if (passwordData.new_password !== passwordData.confirm_password) {
      errors.confirm_password = t("pages.password.errors.password_mismatch");
      isValid = false;
    }

    setPasswordErrors(errors);
    return isValid;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUserData(prev => ({
      ...prev,
      [name]: value
    }));
    
    if (!touched) setTouched(true);
  };

  // Password field change handler
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!validate()) return;
    if (!hasChanges()) {
      setSuccess(t("pages.profile.no_changes"));
      return;
    }

    setIsSaving(true);
    
    try {
      const response = await api.patch('/user/update', {
        user_name: userData.user_name,
        first_name: userData.first_name,
        last_name: userData.last_name
      });

      setInitialData({
        ...userData,
        user_name: response.data.user_name,
        first_name: response.data.first_name,
        last_name: response.data.last_name,
        uuid_id: userData.uuid_id,
        access_rights: userData.access_rights,
        has_password: initialData.has_password
      });

      setUserData({
        ...userData,
        user_name: response.data.user_name,
        first_name: response.data.first_name,
        last_name: response.data.last_name
      });

      setSuccess(t("pages.profile.updated"));
      setTouched(false);
    } catch (err: any) {
      console.error('Update failed:', err);
      setError(err.response?.data?.detail || t("pages.profile.errors.update"));
    } finally {
      setIsSaving(false);
    }
  };

  // Opening the modal window
  const openPasswordModal = () => {
    setIsPasswordModalOpen(true);
    // Reset data on opening
    setPasswordData({
      current_password: '',
      new_password: '',
      confirm_password: ''
    });
    setPasswordErrors({
      current_password: '',
      new_password: '',
      confirm_password: ''
    });
  };

  // Closing the modal window
  const closePasswordModal = () => {
    setIsPasswordModalOpen(false);
  };

  // Password change handler
  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!validatePassword()) return;

    setIsChangingPassword(true);
    
    try {
      await api.patch('/user/password', {
        current_password: initialData.has_password ? passwordData.current_password : undefined,
        new_password: passwordData.new_password,
        confirm_password: passwordData.confirm_password
      });

      setSuccess(t("pages.password.password_updated"));
      setInitialData(prev => ({ ...prev, has_password: true }));
      closePasswordModal();
    } catch (err: any) {
      setError(err.response?.data?.detail || t("pages.password.errors.password_update"));
    } finally {
      setIsChangingPassword(false);
    }
  };

  const handleLogout = () => {
    if (touched && !window.confirm(t("pages.profile.unsaved_changes"))) {
      return;
    }
    logout();
  };

  if (loading) {
    return (
      <div className="text-center py-10">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        <p className="mt-2">{t("pages.profile.loading")}</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="flex items-center gap-3 mb-6">
        <h1 className="text-2xl font-bold">{t("pages.profile.title")}</h1>
        <span className="text-sm text-gray-600">{t("pages.profile.status")}:</span>
        <div className="flex flex-col items-start">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            userData.access_rights === "owner" ? "bg-yellow-100 text-yellow-800" :
            userData.access_rights === "full" ? "bg-green-100 text-green-800" :
            userData.access_rights === "pro" ? "bg-blue-100 text-blue-800" :
            userData.access_rights === "plus" ? "bg-purple-100 text-purple-800" :
            "bg-gray-100 text-gray-800"
          }`}>
            {userData.access_rights}
          </span>
          {accessExpiresAt && (
            <span className="text-xs text-gray-500 mt-1">
              {t("pages.profile.expires_at")}: {new Date(accessExpiresAt).toLocaleDateString()}
            </span>
          )}
        </div>
      </div>
      
      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
          <p>{error}</p>
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
          <p>{success}</p>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
        <div className="mb-4">
          <label htmlFor="user_name" className="block text-gray-700 mb-2">
            {t("pages.profile.username")} *
          </label>
          <input
            id="user_name"
            name="user_name"
            type="text"
            value={userData.user_name}
            onChange={handleInputChange}
            className={`w-full p-2 border rounded ${
              validationErrors.user_name ? 'border-red-500' : ''
            }`}
            aria-label="Username"
            maxLength={50}
            required
          />
          {validationErrors.user_name && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.user_name}</p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label htmlFor="first_name" className="block text-gray-700 mb-2">
              {t("pages.profile.first_name")}
            </label>
            <input
              id="first_name"
              name="first_name"
              type="text"
              value={userData.first_name}
              onChange={handleInputChange}
              className={`w-full p-2 border rounded ${
                validationErrors.first_name ? 'border-red-500' : ''
              }`}
              aria-label={t("pages.profile.first_name")}
              maxLength={100}
            />
            {validationErrors.first_name && (
              <p className="text-red-500 text-sm mt-1">{validationErrors.first_name}</p>
            )}
          </div>
          
          <div>
            <label htmlFor="last_name" className="block text-gray-700 mb-2">
              {t("pages.profile.last_name")}
            </label>
            <input
              id="last_name"
              name="last_name"
              type="text"
              value={userData.last_name}
              onChange={handleInputChange}
              className={`w-full p-2 border rounded ${
                validationErrors.last_name ? 'border-red-500' : ''
              }`}
              aria-label={t("pages.profile.last_name")}
              maxLength={100}
            />
            {validationErrors.last_name && (
              <p className="text-red-500 text-sm mt-1">{validationErrors.last_name}</p>
            )}
          </div>
        </div>

        <div className="mb-6">
          <label htmlFor="email" className="block text-gray-700 mb-2">
            {t("pages.profile.email")}
          </label>
          <input
            id="email"
            type="email"
            value={userData.email}
            disabled
            className="w-full p-2 border rounded bg-gray-100"
            aria-label={t("pages.profile.email_readonly")}
          />
          <p className="text-sm text-gray-500 mt-1">{t("pages.profile.email_not_change")}</p>
        </div>
        
        <div className="flex flex-wrap justify-between gap-4">
          <button
            type="submit"
            disabled={isSaving || (!hasChanges() && !touched)}
            className={`bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex-1 ${
              isSaving || (!hasChanges() && !touched) ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            aria-label={t("pages.profile.save")}
          >
            {isSaving ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {t("pages.profile.saving")}
              </span>
            ) : (
              t("pages.profile.save")
            )}
          </button>
          
          <button 
            type="button"
            onClick={openPasswordModal}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 flex-1"
            aria-label={initialData.has_password ? t("pages.password.change_password") : t("pages.password.set_password")}
          >
            {initialData.has_password 
              ? t("pages.password.change_password") 
              : t("pages.password.set_password")
            }
          </button>
          
          <button 
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 flex-1"
            aria-label={t("pages.profile.logout")}
          >
            {t("pages.profile.logout")}
          </button>
        </div>
      </form>

      {/* Modal window for changing the password */}
      {isPasswordModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-lg w-full max-w-md">
            <div className="p-6">
              <h2 className="text-xl font-bold mb-4">
                {initialData.has_password 
                  ? t("pages.password.change_password") 
                  : t("pages.password.set_password")
                }
              </h2>
              
              <form onSubmit={handlePasswordSubmit}>
                {initialData.has_password && (
                  <div className="mb-4">
                    <label htmlFor="current_password" className="block text-gray-700 mb-2">
                      {t("pages.password.current_password")} *
                    </label>
                    <input
                      id="current_password"
                      name="current_password"
                      type="password"
                      value={passwordData.current_password}
                      onChange={handlePasswordChange}
                      className={`w-full p-2 border rounded ${
                        passwordErrors.current_password ? 'border-red-500' : ''
                      }`}
                      aria-label={t("pages.password.current_password")}
                    />
                    {passwordErrors.current_password && (
                      <p className="text-red-500 text-sm mt-1">{passwordErrors.current_password}</p>
                    )}
                  </div>
                )}

                <div className="mb-4">
                  <label htmlFor="new_password" className="block text-gray-700 mb-2">
                    {t("pages.password.new_password")} *
                  </label>
                  <input
                    id="new_password"
                    name="new_password"
                    type="password"
                    value={passwordData.new_password}
                    onChange={handlePasswordChange}
                    className={`w-full p-2 border rounded ${
                      passwordErrors.new_password ? 'border-red-500' : ''
                    }`}
                    aria-label={t("pages.password.new_password")}
                  />
                  {passwordErrors.new_password && (
                    <p className="text-red-500 text-sm mt-1">{passwordErrors.new_password}</p>
                  )}
                  <p className="text-sm text-gray-500 mt-1">{t("pages.password.password_requirements")}</p>
                </div>

                <div className="mb-6">
                  <label htmlFor="confirm_password" className="block text-gray-700 mb-2">
                    {t("pages.password.confirm_password")} *
                  </label>
                  <input
                    id="confirm_password"
                    name="confirm_password"
                    type="password"
                    value={passwordData.confirm_password}
                    onChange={handlePasswordChange}
                    className={`w-full p-2 border rounded ${
                      passwordErrors.confirm_password ? 'border-red-500' : ''
                    }`}
                    aria-label={t("pages.password.confirm_password")}
                  />
                  {passwordErrors.confirm_password && (
                    <p className="text-red-500 text-sm mt-1">{passwordErrors.confirm_password}</p>
                  )}
                </div>

                <div className="flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={closePasswordModal}
                    className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100"
                    aria-label={t("pages.cancel")}
                  >
                    {t("pages.cancel")}
                  </button>
                  <button
                    type="submit"
                    disabled={isChangingPassword}
                    className={`bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 ${
                      isChangingPassword ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                  >
                    {isChangingPassword ? (
                      <span className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        {t("pages.profile.saving")}
                      </span>
                    ) : (
                      initialData.has_password 
                        ? t("pages.password.change_button") 
                        : t("pages.password.set_button")
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
