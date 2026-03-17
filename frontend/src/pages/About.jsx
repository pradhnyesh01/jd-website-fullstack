import aboutImage from "../assets/heroabout.jpeg";

export default function About() {
  return (
    <div>

      {/* Banner */}
      <section className="bg-gradient-to-r from-blue-900 to-blue-700 text-white py-24">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h1 className="text-4xl font-bold">
            About J.D. Enterprises
          </h1>
          <p className="mt-4 text-gray-200 max-w-3xl mx-auto">
            ISO 9001:2015 Certified • ‘A’ Class Government Electrical Contractor • Established 2010
          </p>
        </div>
      </section>

      {/* Company Overview */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

          {/* Text */}
          <div>
            <h2 className="text-3xl font-bold text-blue-900 mb-6">
              Company Overview
            </h2>

            <p className="text-gray-700 mb-6 leading-relaxed">
              J.D. Enterprises is an ISO 9001:2015 certified ‘A’ Class Government 
              Electrical Contractor specializing in contracting and execution of 
              advanced Audio Visual, Surveillance and Lighting systems.
            </p>

            <p className="text-gray-700 mb-6 leading-relaxed">
              We provide complete end-to-end solutions including Sound Systems, 
              LED Displays, Video Walls, Video Conference Systems, Stage Lighting, 
              Stage Craft, CCTV Surveillance, LAN Networking and Projection Systems.
            </p>

            <p className="text-gray-700 leading-relaxed">
              Our services include technical consultancy, site-specific system 
              design, supply, installation and commissioning — ensuring optimal 
              sound clarity, performance and long-term reliability.
            </p>
          </div>

          {/* Image */}
          <div>
            <img
              src={aboutImage}
              alt="J.D. Enterprises Installation Work"
              className="rounded-xl shadow-xl w-full object-cover border border-gray-200"
            />
          </div>

        </div>
      </section>

      {/* History */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-blue-900 mb-6">
            Our Journey
          </h2>

          <p className="text-gray-700 leading-relaxed">
            Established in 2010, J.D. Enterprises has built industry leadership 
            through more than 16 years of unwavering commitment to customer 
            satisfaction. Our philosophy is consistent evolution — adopting 
            modern technologies instead of relying on obsolete systems.
          </p>

          <p className="text-gray-700 mt-6 leading-relaxed">
            Through a strong marketing network and prompt service support, 
            we have developed a prestigious client base including Government 
            Departments, Defense establishments, Corporate organizations, 
            Educational institutions and Industrial clients across Maharashtra.
          </p>
        </div>
      </section>

      {/* Core Values */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6">

          <h2 className="text-3xl font-bold text-blue-900 mb-16 text-center">
            Our Core Values
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">

            <ValueCard
              title="Our Pledge"
              description="To achieve customer satisfaction through integrity and time-bound commitments."
            />

            <ValueCard
              title="Our Passion"
              description="Continuous endeavor towards updated knowledge and technological advancement."
            />

            <ValueCard
              title="Our Mission"
              description="To provide neat, structured and user-friendly systems through dedicated and disciplined teamwork."
            />

            <ValueCard
              title="Our Approach"
              description="We transform discourse into dialogue. Whether a conference or performance, every listener should feel a one-to-one connection."
            />

            <ValueCard
              title="Our Commitment"
              description="The Best Is Yet To Be — We strive for excellence in every project we execute."
            />

          </div>
        </div>
      </section>

      {/* Industries Served */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-blue-900 mb-12">
            Industries We Serve
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-gray-700 font-medium">
            <div>Government Departments</div>
            <div>Defense Establishments</div>
            <div>Educational Institutions</div>
            <div>Corporate Offices</div>
            <div>Hospitals</div>
            <div>Auditoriums & Conference Halls</div>
            <div>Sports Stadiums</div>
            <div>Industrial Facilities</div>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6 text-center">

          <h2 className="text-3xl font-bold text-blue-900 mb-16">
            Why Choose J.D. Enterprises
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-10 text-left">

            <FeatureCard
              title="ISO 9001:2015 Certified"
              description="Quality-driven processes ensuring consistency, reliability and professional standards."
            />

            <FeatureCard
              title="Government Approved Contractor"
              description="Authorized ‘A’ Class Electrical Contractor compliant with government regulations and procurement systems."
            />

            <FeatureCard
              title="Turnkey Project Execution"
              description="From consultation and design to installation, commissioning and ongoing service support."
            />

          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-blue-900 text-white py-20">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="text-3xl font-bold">
            Building Smart, Secure & Technologically Advanced Infrastructure
          </h2>
          <p className="mt-4 text-gray-200">
            Partner with J.D. Enterprises for reliable, scalable and future-ready solutions.
          </p>
        </div>
      </section>

    </div>
  );
}

/* Components */

function ValueCard({ title, description }) {
  return (
    <div className="border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition">
      <h3 className="text-xl font-semibold text-blue-800 mb-3">
        {title}
      </h3>
      <p className="text-gray-600 text-sm leading-relaxed">
        {description}
      </p>
    </div>
  );
}

function FeatureCard({ title, description }) {
  return (
    <div>
      <h4 className="font-semibold text-blue-800 mb-3 text-lg">
        {title}
      </h4>
      <p className="text-gray-600 text-sm leading-relaxed">
        {description}
      </p>
    </div>
  );
}
