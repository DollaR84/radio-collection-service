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
            <p className="text-xs text-gray-400">Accessibility-first design</p>
          </div>
          <div className="mt-4 md:mt-0">
            <p className="text-sm">
              Contact: 
              <a href="mailto:elrus-admin@s2.ho.ua" className="ml-2 text-blue-300 hover:underline">
                Send Email ElrusApps
              </a>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
