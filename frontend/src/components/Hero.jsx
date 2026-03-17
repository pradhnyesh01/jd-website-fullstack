import { useEffect, useState } from "react";
import hero1 from "../assets/herocctv.jpg";
import hero2 from "../assets/heroprojector.jpg";
import hero3 from "../assets/herospeaker.jpg";

const images = [hero1, hero2, hero3];

export default function Hero({ onOpenModal }) {
  const [currentIndex, setCurrentIndex] = useState(0);

  // Auto slide every 4 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % images.length);
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <section className="relative min-h-[85vh] md:min-h-screen flex items-center overflow-hidden">

      {/* Background Slides */}
      {images.map((image, index) => (
        <div
          key={index}
          className={`absolute inset-0 transition-opacity duration-1000 ${
            index === currentIndex ? "opacity-100" : "opacity-0"
          }`}
        >
          <img
            src={image}
            alt="J.D. Enterprises Solutions"
            className="w-full h-full object-cover"
          />
        </div>
      ))}

      {/* Overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-950/90 via-blue-900/85 to-blue-800/80"></div>

      {/* Content */}
      <div className="relative w-full px-6 md:px-10 lg:px-24 xl:px-36 py-16 md:py-20">

        <div className="max-w-6xl space-y-8 md:space-y-10 text-white">

          {/* Badge */}
          <div className="inline-block bg-white/20 text-xs sm:text-sm px-5 py-2 rounded-full font-medium backdrop-blur-sm">
            ISO 9001:2015 Certified • ‘A’ Class Government Electrical Contractor • Since 2010
          </div>

          {/* Heading */}
          <h1 className="text-3xl sm:text-4xl md:text-5xl xl:text-6xl font-bold leading-tight">
            Integrated Audio Visual,
            <br />
            Surveillance & Lighting
            <br />
            Solutions
          </h1>

          {/* Description */}
          <p className="text-base md:text-lg text-gray-200 max-w-3xl">
            Delivering professional sound systems, CCTV infrastructure,
            LED displays, video conferencing and networking solutions
            for government, corporate and institutional spaces.
          </p>

          {/* Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 md:gap-10 pt-6 md:pt-8 text-sm">
            <div>
              <div className="text-2xl md:text-3xl font-bold">16+</div>
              <div className="text-gray-200">Years Experience</div>
            </div>
            <div>
              <div className="text-2xl md:text-3xl font-bold">500+</div>
              <div className="text-gray-200">Projects Executed</div>
            </div>
            <div>
              <div className="text-2xl md:text-3xl font-bold">Govt.</div>
              <div className="text-gray-200">Approved Contractor</div>
            </div>
            <div>
              <div className="text-2xl md:text-3xl font-bold">Maharashtra</div>
              <div className="text-gray-200">Statewide Operations</div>
            </div>
          </div>

          {/* Buttons */}
          <div className="flex gap-4 flex-wrap pt-4 md:pt-6">
            <button
              onClick={onOpenModal}
              className="bg-white text-blue-900 px-6 md:px-8 py-3 font-semibold rounded-md hover:scale-105 transition"
            >
              Request a Quote
            </button>

            <a
              href="#services"
              className="border border-white px-6 md:px-8 py-3 font-semibold rounded-md hover:bg-white hover:text-blue-900 transition"
            >
              Explore Services
            </a>
          </div>

        </div>
      </div>
    </section>
  );
}
