import { useEffect, useRef, useState } from "react";
import emailjs from "@emailjs/browser";

const SYSTEM_TO_SERVICE = {
  "CCTV": "CCTV Surveillance",
  "Perimeter Security": "CCTV Surveillance",
  "Access Control": "CCTV Surveillance",
  "Sound System": "Audio Systems",
  "PA System": "Audio Systems",
  "AV Systems": "Audio Systems",
  "Video Conferencing": "Audio Systems",
  "Stage Lighting": "Lighting Systems",
  "Lighting": "Lighting Systems",
  "Projection": "LCD Projectors",
  "LED Display": "LCD Projectors",
};

function buildPrefillMessage(prefillData) {
  if (!prefillData) return "";
  const systems = Object.keys(prefillData.systems || {});
  const lines = [
    `Facility: ${prefillData.facility || "—"}`,
    `Size: ${prefillData.size || "—"}`,
    `Setup: ${prefillData.setup_type || "—"}`,
    `Systems required: ${systems.join(", ")}`,
  ];
  if (prefillData.budget_tier) lines.push(`Budget range: ${prefillData.budget_tier}`);
  return lines.join("\n");
}

function detectService(prefillData) {
  if (!prefillData) return "";
  for (const system of Object.keys(prefillData.systems || {})) {
    if (SYSTEM_TO_SERVICE[system]) return SYSTEM_TO_SERVICE[system];
  }
  return "";
}

export default function QuoteModal({ isOpen, onClose, prefillData }) {
  const formRef = useRef();
  const serviceRef = useRef();
  const messageRef = useRef();
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Close on ESC key
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  // Apply prefill data when modal opens with chat data
  useEffect(() => {
    if (isOpen && prefillData) {
      if (serviceRef.current) {
        const matched = detectService(prefillData);
        if (matched) serviceRef.current.value = matched;
      }
      if (messageRef.current) {
        messageRef.current.value = buildPrefillMessage(prefillData);
      }
    }
  }, [isOpen, prefillData]);

  // Auto close after successful submission
  useEffect(() => {
    if (isSubmitted) {
      const timer = setTimeout(() => {
        setIsSubmitted(false);
        onClose();
      }, 2500);
      return () => clearTimeout(timer);
    }
  }, [isSubmitted, onClose]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = formRef.current;
    if (form.company?.value) return; // honeypot

    setIsLoading(true);
    emailjs
      .sendForm(
        import.meta.env.VITE_EMAIL_SERVICE_ID,
        import.meta.env.VITE_EMAIL_TEMPLATE_ID,
        form,
        import.meta.env.VITE_EMAIL_PUBLIC_KEY
      )
      .then(() => {
        setIsSubmitted(true);
        setIsLoading(false);
        form.reset();
      })
      .catch((error) => {
        console.error("EmailJS Error:", error);
        setIsLoading(false);
      });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">

      {/* Overlay */}
      <div
        className="absolute inset-0 bg-black/40 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="relative bg-white w-full max-w-lg mx-4 rounded-lg shadow-xl p-8">

        {isSubmitted ? (
          <div className="text-center py-8">
            <div className="text-green-600 text-5xl mb-4">✓</div>
            <h3 className="text-xl font-semibold text-blue-800 mb-2">
              Request Sent Successfully!
            </h3>
            <p className="text-gray-600">Our team will contact you shortly.</p>
          </div>
        ) : (
          <>
            <h2 className="text-2xl font-bold text-blue-800 mb-1">
              Request a Quote
            </h2>
            {prefillData && (
              <p className="text-sm text-green-700 mb-4">
                ✅ Pre-filled from your AI recommendation — review and submit.
              </p>
            )}

            <form ref={formRef} onSubmit={handleSubmit} className="space-y-4">

              {/* Honeypot Field (Hidden) */}
              <input
                type="text"
                name="company"
                style={{ display: "none" }}
                tabIndex="-1"
                autoComplete="off"
              />

              <input
                type="text"
                name="user_name"
                placeholder="Full Name"
                required
                className="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
              />

              <input
                type="email"
                name="user_email"
                placeholder="Email Address"
                required
                className="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
              />

              <input
                type="tel"
                name="user_phone"
                placeholder="Phone Number"
                required
                className="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
              />

              <select
                ref={serviceRef}
                name="service"
                required
                className="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select Service</option>
                <option>Audio Systems</option>
                <option>CCTV Surveillance</option>
                <option>LCD Projectors</option>
                <option>Lighting Systems</option>
              </select>

              <textarea
                ref={messageRef}
                name="message"
                rows="4"
                placeholder="Project Details"
                required
                className="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
              ></textarea>

              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={onClose}
                  disabled={isLoading}
                  className="px-4 py-2 border rounded-md hover:bg-gray-100 disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-6 py-2 bg-blue-700 text-white rounded-md hover:bg-blue-800 disabled:opacity-50"
                >
                  {isLoading ? "Sending..." : "Submit"}
                </button>
              </div>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
