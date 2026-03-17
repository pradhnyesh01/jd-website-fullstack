export default function ServiceBlock({
  title,
  description,
  points,
  image,
  reverse = false,
}) {
  return (
    <section className="py-24 bg-white">
      <div
        className={`max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center ${
          reverse ? "lg:[&>*:first-child]:order-2" : ""
        }`}
      >
        {/* Image Section */}
        <div className="relative w-full">
          <img
            src={image}
            alt={title}
            className="rounded-2xl shadow-2xl w-full h-[420px] object-cover"
          />

          {/* Subtle overlay effect */}
          <div className="absolute inset-0 rounded-2xl ring-1 ring-black/5"></div>
        </div>

        {/* Content Section */}
        <div className="w-full">
          <h2 className="text-3xl lg:text-4xl font-bold text-blue-900 mb-6 leading-snug">
            {title}
          </h2>

          <p className="text-gray-700 mb-8 leading-relaxed text-base">
            {description}
          </p>

          <ul className="space-y-4">
            {points.map((point, index) => (
              <li
                key={index}
                className="flex items-start gap-4 text-gray-600 text-sm lg:text-base"
              >
                <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-blue-100 text-blue-700 font-semibold text-xs mt-1">
                  ✓
                </span>
                <span className="leading-relaxed">{point}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
