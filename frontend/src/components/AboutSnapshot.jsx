import { Link } from "react-router-dom";
import aboutImage from "../assets/heroabout.jpeg";

export default function AboutSnapshot() {
  return (
    <section className="py-20 bg-gray-50 animate-fadeUp">
      <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

        {/* Text */}
        <div>
          <h2 className="text-3xl font-bold text-blue-800 mb-6">
            About J.D. Enterprises
          </h2>

          <p className="text-gray-700 mb-6">
            J.D. Enterprises is an ISO 9001:2015 certified ‘A’ Class Government Electrical Contractor 
            delivering integrated audio-visual, surveillance and lighting solutions for government departments, 
            corporate offices, educational institutions and industrial facilities.
          </p>

          <p className="text-gray-700 mb-6">
            Established in 2010, we have built a strong reputation across Maharashtra 
            through consistent technological advancement, 
            regulatory compliance and professionally executed turnkey projects.
          </p>

          <Link
            to="/about"
            className="inline-block bg-blue-700 text-white px-6 py-3 rounded-md font-semibold hover:bg-blue-800 transition"
          >
            Read More →
          </Link>
        </div>

        {/* Image */}
        <div>
          <img
            src={aboutImage}
            alt="Professional Installation Work"
            className="rounded-xl shadow-lg w-full object-cover"
          />

        </div>

      </div>
    </section>
  );
}
