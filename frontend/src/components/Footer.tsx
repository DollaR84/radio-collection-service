import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-4 mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-sm">© {new Date().getFullYear()} RadioCollection Service</p>
          </div>
          <div className="text-center">
            <p className="text-sm">Created by ElrusApps</p>
            <p className="text-sm">Author: Dolovaniuk Ruslan</p>
            <p className="text-xs text-gray-400">Accessibility-first design</p>
          </div>
          <div className="mt-4 md:mt-0">
            <p className="text-sm">
              Contact: 
              <a href="mailto:elrus-admin@s2.ho.ua" className="ml-2 text-blue-300 hover:underline">
                Send Email ElrusApps
              </a>
            </p>
            <Link
              to="/donate"
              className="ml-0 md:ml-4 px-3 py-1 bg-yellow-500 hover:bg-yellow-600 rounded
text-black text-sm transition"              
            >
              Donate...
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
