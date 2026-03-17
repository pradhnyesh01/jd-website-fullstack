import { MapPin, Phone, Mail } from "lucide-react";
import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="bg-blue-950 text-gray-300 pt-16 pb-8 mt-20">

      <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12">

        {/* Company Info */}
        <div>
          <h3 className="text-xl font-semibold text-white mb-4">
            J.D. Enterprises
          </h3>

          <p className="text-sm mb-2">
            ISO 9001:2015 Certified
          </p>

          <p className="text-sm mb-2">
            ‘A’ Class Government Electrical Contractor
          </p>

          <p className="text-sm mb-2">
            Established 2010
          </p>

          <p className="text-sm">
            GST No: 27AJTPD1488P1ZD
          </p>
        </div>

        {/* Services */}
        <div>
          <h3 className="text-xl font-semibold text-white mb-4">
            Solutions
          </h3>

          <ul className="space-y-2 text-sm">
            <li>
              <Link to="/services" className="hover:text-white transition">
                Sound & Public Address Systems
              </Link>
            </li>
            <li>
              <Link to="/services" className="hover:text-white transition">
                CCTV & Surveillance Infrastructure
              </Link>
            </li>
            <li>
              <Link to="/services" className="hover:text-white transition">
                LED Displays & Video Walls
              </Link>
            </li>
            <li>
              <Link to="/services" className="hover:text-white transition">
                Projection & Presentation Systems
              </Link>
            </li>
            <li>
              <Link to="/services" className="hover:text-white transition">
                Stage Lighting & Networking
              </Link>
            </li>
          </ul>
        </div>

        {/* Contact Info */}
        <div>
          <h3 className="text-xl font-semibold text-white mb-4">
            Contact Information
          </h3>

          <div className="space-y-4 text-sm">

            <div className="flex items-start gap-3">
              <MapPin size={16} className="mt-1 flex-shrink-0" />
              <span>
                Flat No. 3 & 4, 1st Floor,<br />
                Hari Om Empire Building,<br />
                Gokhale Nagar Road,<br />
                Shivajinagar, Pune – 411016
              </span>
            </div>

            <div className="flex items-center gap-3">
              <Phone size={16} />
              <a
                href="tel:+919422317544"
                className="hover:text-white transition"
              >
                +91 94223 17544
              </a>
            </div>

            <div className="flex items-center gap-3">
              <Mail size={16} />
              <a
                href="mailto:jcd5175@gmail.com"
                className="hover:text-white transition"
              >
                jcd5175@gmail.com
              </a>
            </div>

          </div>
        </div>

      </div>

      {/* Bottom Strip */}
      <div className="border-t border-blue-800 mt-12 pt-6 text-center text-sm text-gray-400">
        © {new Date().getFullYear()} J.D. Enterprises. All Rights Reserved.
      </div>

    </footer>
  );
}
