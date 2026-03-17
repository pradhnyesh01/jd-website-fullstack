import ServiceBlock from "../components/ServiceBlock";

import audioImage from "../assets/speakers.jpg";
import cctvImage from "../assets/cctv.jpg";
import projectorImage from "../assets/projector.jpg";
import lightingImage from "../assets/lighting.jpg";
import networkImage from "../assets/network.jpg";

export default function Services() {
  return (
    <div>

      {/* Page Banner */}
      <section className="bg-gradient-to-r from-blue-900 to-blue-700 text-white py-24">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h1 className="text-4xl font-bold">
            Integrated AV & Surveillance Solutions
          </h1>
          <p className="mt-4 text-gray-200 max-w-3xl mx-auto">
            J.D. Enterprises delivers complete design, supply, installation and
            commissioning services for audio-visual, security and communication
            infrastructure across government, corporate and institutional sectors.
          </p>
        </div>
      </section>

      {/* Professional Sound Systems */}
      <ServiceBlock
        title="Professional Sound & Public Address Systems"
        description="We design and deploy high-performance sound systems tailored for auditoriums, conference halls, educational institutions and public facilities — ensuring clarity, coverage and reliability."
        points={[
          "Public Address & Announcement Systems",
          "Conference & Boardroom Audio Solutions",
          "Auditorium Acoustic Installations",
          "Digital Mixers, Amplifiers & Wireless Microphones",
          "Annual Maintenance & System Support",
        ]}
        image={audioImage}
      />

      {/* CCTV Surveillance */}
      <ServiceBlock
        title="CCTV & Integrated Surveillance Infrastructure"
        description="Comprehensive security solutions including camera networks, monitoring stations and secure recording systems for institutions, industries and government facilities."
        points={[
          "IP-Based & Analog Camera Systems",
          "Centralized Monitoring & Control Rooms",
          "Night Vision & Perimeter Security Systems",
          "Remote Viewing & Network Integration",
          "Preventive Maintenance & AMC Services",
        ]}
        image={cctvImage}
        reverse
      />

      {/* Projection & Display */}
      <ServiceBlock
        title="Projection, LED Displays & Video Walls"
        description="Advanced visual communication systems designed for classrooms, corporate boardrooms, auditoriums and command centers."
        points={[
          "Ceiling-Mounted & High-Lumen Projectors",
          "Interactive Smart Boards & Presentation Systems",
          "Large-Format LED Displays",
          "Video Wall Installation & Configuration",
          "System Calibration & Optimization",
        ]}
        image={projectorImage}
      />

      {/* Lighting & Stage Craft */}
      <ServiceBlock
        title="Stage Lighting & Architectural Lighting Systems"
        description="Modern lighting solutions for performance venues, commercial spaces and institutional environments with intelligent control systems."
        points={[
          "Stage & Event Lighting Design",
          "Architectural & Facade Lighting",
          "Energy-Efficient LED Installations",
          "Lighting Control & Automation Systems",
          "Complete Stage Craft Setup",
        ]}
        image={lightingImage}
        reverse
      />

      {/* Networking & Consultancy */}
      <ServiceBlock
        title="LAN Networking & Technical Consultancy"
        description="Structured cabling and network infrastructure designed to support integrated audio-visual and surveillance systems with long-term scalability."
        points={[
          "Structured Cabling & Rack Installations",
          "Network Infrastructure Planning",
          "Site-Specific System Design",
          "Technical Evaluation & Acoustic Consultation",
          "End-to-End Project Execution",
        ]}
        image={networkImage} // Replace with networking image later if available
      />

      {/* CTA */}
      <section className="bg-blue-900 text-white py-20 mt-20">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="text-3xl font-bold">
            Planning to Upgrade Your Facility Infrastructure?
          </h2>
          <p className="mt-4 text-gray-200">
            Partner with J.D. Enterprises for reliable, future-ready and
            government-compliant technology solutions.
          </p>
        </div>
      </section>

    </div>
  );
}
