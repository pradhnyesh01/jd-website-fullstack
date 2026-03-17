import { Link } from "react-router-dom";

export default function ServicesSection() {
  return (
    <section id="services" className="bg-white py-24">
      <div className="max-w-7xl mx-auto px-6">

        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-blue-900">
            Comprehensive Technology Solutions
          </h2>
          <p className="mt-4 text-gray-600 max-w-3xl mx-auto">
            We design, implement and maintain integrated audio-visual,
            surveillance and communication systems tailored for government,
            corporate and institutional environments.
          </p>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">

          {/* Service 1 */}
          <ServiceCard
            title="Professional Sound Systems"
            description="Advanced public address systems, auditorium acoustics, conference audio setups and high-performance amplification solutions designed for clarity and reliability."
          />

          {/* Service 2 */}
          <ServiceCard
            title="Video Conferencing & Collaboration"
            description="End-to-end conferencing solutions including cameras, control systems and integrated communication platforms for seamless virtual collaboration."
          />

          {/* Service 3 */}
          <ServiceCard
            title="LED Displays & Video Walls"
            description="High-definition LED screens and large-format video wall installations for control rooms, auditoriums, events and information display systems."
          />

          {/* Service 4 */}
          <ServiceCard
            title="CCTV & Security Surveillance"
            description="Comprehensive surveillance infrastructure including IP cameras, recording systems, monitoring setups and network-based security integration."
          />

          {/* Service 5 */}
          <ServiceCard
            title="Projection & Presentation Systems"
            description="Professional-grade projection systems for classrooms, boardrooms and large venues with precise calibration and installation."
          />

          {/* Service 6 */}
          <ServiceCard
            title="Stage Lighting & Stage Craft"
            description="Dynamic lighting solutions and stage infrastructure for auditoriums, performances and institutional events with modern control systems."
          />

          {/* Service 7 */}
          <ServiceCard
            title="LAN Networking Solutions"
            description="Structured cabling, networking infrastructure and connectivity solutions to support audio-visual and surveillance systems."
          />

          {/* Service 8 */}
          <ServiceCard
            title="Technical Consultancy & Design"
            description="Site-specific system planning, acoustic consultation and technical guidance to ensure optimal system performance and long-term scalability."
          />

        </div>

      </div>
    </section>
  );
}

/* Reusable Service Card Component */

function ServiceCard({ title, description }) {
  return (
    <div className="bg-gray-50 p-8 rounded-lg shadow-sm hover:shadow-xl hover:-translate-y-2 transition duration-300 flex flex-col justify-between">
      
      <div>
        <h3 className="text-xl font-semibold text-blue-800 mb-4">
          {title}
        </h3>

        <p className="text-gray-600 text-sm leading-relaxed">
          {description}
        </p>
      </div>

      <Link
        to="/services"
        className="mt-8 text-blue-800 font-semibold hover:underline"
      >
        Discover More →
      </Link>

    </div>
  );
}
