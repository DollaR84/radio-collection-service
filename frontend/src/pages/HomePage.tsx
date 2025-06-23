import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function HomePage() {
  const { token } = useAuth();

  return (
    <div className="text-center max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">Welcome to Radio Collection</h1>

      <p className="mb-4 text-lg">
        Radio Collection is a project dedicated to discovering, organizing, and listening to your favorite online radio stations — all in one place.
      </p>

      <p className="mb-4 text-lg">
        I'm a blind developer from Ukraine, passionate about accessibility and open technologies.
        This service is designed with screen reader support in mind — especially optimized for NVDA —
        and includes a public API that can be used by radio clients and other developers.
      </p>

      <p className="mb-4 text-lg">
        You can explore all my open-source projects on my{" "}
        <a href="https://github.com/DollaR84" className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">
          GitHub account
        </a>.
      </p>

      <div className="mb-6 text-lg">
        <p>📨 Contact:{" "}
          <a href="mailto:elrus-admin@s2.ho.ua" className="text-blue-500 underline">
            support email
          </a>
        </p>
        <p>📢 Telegram Channel:{" "}
          <a href="https://t.me/elrusapps" className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">
            @elrusapps
          </a>
        </p>
        <p>💬 Telegram Group:{" "}
          <a href="https://t.me/elrus_apps" className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">
            @elrus_apps
          </a>
        </p>
      </div>

      {!token && (
        <Link to="/login" className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 text-lg">
          Login to start listening
        </Link>
      )}
    </div>
  );
}
