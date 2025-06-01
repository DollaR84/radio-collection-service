import { Outlet, useNavigate } from 'react-router-dom';
export default function Layout() {
const navigate = useNavigate();
const handleLogout = () => {
localStorage.removeItem('token');
navigate('/login');
};
return (
<div>
<header className="bg-gray-800 text-white p-4">
<div className="container mx-auto flex justify-between items-center">
<nav>
<ul className="flex space-x-4">
<li><button onClick={() => navigate('/stations')}>Станции</button></li>
<li><button onClick={() => navigate('/profile')}>Профиль</button></li>
</ul>
</nav>
<button onClick={handleLogout}>Logout</button>
</div>
</header>
<main className="container mx-auto p-4">
<Outlet />
</main>
</div>
);
}
