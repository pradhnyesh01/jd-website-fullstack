import { NavLink } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Navbar({ onOpenModal, onOpenChat }) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  // Detect scroll
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`sticky top-0 z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-white shadow-lg py-4"
          : "bg-white py-6"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 flex justify-between items-center">

        {/* Logo */}
        <div className="flex items-center gap-3">
          <img
            src="/logo.png"
            alt="J.D. Enterprises"
            className={`transition-all duration-300 ${
              isScrolled ? "h-10" : "h-12"
            }`}
          />
          <span className="font-bold text-lg text-blue-900">
            J.D. Enterprises
          </span>
        </div>

        {/* Desktop Menu */}
        <div className="hidden md:flex items-center gap-6 text-gray-700">

          {["/", "/about", "/services", "/contact"].map((path, i) => {
            const labels = ["Home", "About", "Services", "Contact"];
            return (
              <NavLink
                key={path}
                to={path}
                className={({ isActive }) =>
                  isActive
                    ? "border-b-2 border-blue-700 pb-1 font-semibold text-blue-800"
                    : "hover:text-blue-700 transition"
                }
              >
                {labels[i]}
              </NavLink>
            );
          })}

          <div className="flex items-center gap-3">
            <button
              onClick={onOpenModal}
              className="bg-blue-700 text-white px-4 py-2 rounded-md hover:bg-blue-800 transition"
            >
              Get Quote
            </button>

            <button
              onClick={onOpenChat}
              className="border border-blue-700 text-blue-700 px-4 py-2 rounded-md hover:bg-blue-50 transition"
            >
              What Do I Need?
            </button>
          </div>
        </div>

        {/* Mobile Toggle */}
        <button
          className="md:hidden text-blue-900"
          onClick={() => setIsOpen(!isOpen)}
        >
          ☰
        </button>
      </div>

      {/* Mobile Dropdown */}
      {isOpen && (
        <div className="md:hidden bg-white shadow-md px-6 py-4 space-y-4">
          {["/", "/about", "/services", "/contact"].map((path, i) => {
            const labels = ["Home", "About", "Services", "Contact"];
            return (
              <NavLink
                key={path}
                to={path}
                onClick={() => setIsOpen(false)}
                className="block"
              >
                {labels[i]}
              </NavLink>
            );
          })}

          <button
            onClick={() => {
              onOpenModal();
              setIsOpen(false);
            }}
            className="w-full bg-blue-700 text-white px-4 py-2 rounded-md"
          >
            Get Quote
          </button>

          <button
            onClick={() => {
              onOpenChat();
              setIsOpen(false);
            }}
            className="w-full border border-blue-700 text-blue-700 px-4 py-2 rounded-md"
          >
            What Do I Need?
          </button>
        </div>
      )}
    </nav>
  );
}
