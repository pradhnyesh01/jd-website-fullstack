import { MapPin, Phone, Mail } from "lucide-react";

export default function Contact() {
  return (
    <div>

      {/* Banner */}
      <section className="bg-gradient-to-r from-blue-700 to-blue-500 text-white py-20">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h1 className="text-4xl font-bold">Contact Us</h1>
          <p className="mt-4 text-gray-100 max-w-2xl mx-auto">
            Get in touch with J.D. Enterprises for professional installation and consultation.
          </p>
        </div>
      </section>

      {/* Contact Information */}
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8">

          <div className="bg-gray-50 p-8 rounded-xl shadow-md">
            <div className="flex items-center gap-3 mb-4">
              <MapPin className="text-blue-700" size={22} />
              <h3 className="text-xl font-semibold text-blue-800">
                Address
              </h3>
            </div>

            <p className="text-gray-700 leading-relaxed">
              Flat No. 3, 1st Floor,<br />
              Hari Om Empire Building,<br />
              Gokhale Nagar Road,<br />
              Pune - 411016
            </p>
          </div>



          {/* Phone */}
          <div className="bg-gray-50 p-8 rounded-xl shadow-md">
            <div className="flex items-center gap-3 mb-4">
              <Phone className="text-blue-700" size={22} />
              <h3 className="text-xl font-semibold text-blue-800">
                Mobile
              </h3>
            </div>

            <div className="space-y-2">
              <a
                href="tel:+919422317544"
                className="block text-blue-700 hover:underline"
              >
                +91 94223 17544
              </a>

              <a
                href="tel:+919373309584"
                className="block text-blue-700 hover:underline"
              >
                +91 93733 09584
              </a>
            </div>
          </div>



          {/* Email */}
          <div className="bg-gray-50 p-8 rounded-xl shadow-md">
            <div className="flex items-center gap-3 mb-4">
              <Mail className="text-blue-700" size={22} />
              <h3 className="text-xl font-semibold text-blue-800">
                Email
              </h3>
            </div>

            <a
              href="mailto:jcd5175@gmail.com"
              className="text-blue-700 hover:underline"
            >
              jcd5175@gmail.com
            </a>
          </div>
        </div>
      </section>

      {/* Google Map Embed */}
      <section className="pb-20">
        <div className="max-w-6xl mx-auto px-6">
          <div className="rounded-xl overflow-hidden shadow-lg">
            <iframe
              title="Company Location"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3782.989292933719!2d73.82942047541842!3d18.529385982565884!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bc2bf7843de4fb7%3A0x7af4f26b7eb85ce9!2sHari%20Om%20Empire!5e0!3m2!1sen!2sin!4v1770985016433!5m2!1sen!2sin"
              width="100%"
              height="450"
              style={{ border: 0 }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>
        </div>
      </section>


    </div>
  );
}
