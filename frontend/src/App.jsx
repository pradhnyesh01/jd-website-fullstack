import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import Navbar from "./components/Navbar";
import QuoteModal from "./components/QuoteModal";
import ScrollToTop from "./components/ScrollToTop";
import Footer from "./components/Footer";
import ChatAssistant from "./components/ChatAssistant";

import Home from "./pages/Home";
import About from "./pages/About";
import Services from "./pages/Services";
import Projects from "./pages/Projects";
import Contact from "./pages/Contact";

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  return (
    <>
      <Navbar 
        onOpenModal={() => setIsModalOpen(true)} 
        onOpenChat={() => setIsChatOpen(true)}
      />
      <ScrollToTop />

      <div>
        <Routes>
          <Route path="/" element={<Home onOpenModal={() => setIsModalOpen(true)} />} />
          <Route path="/about" element={<About />} />
          <Route path="/services" element={<Services />} />
          {/*<Route path="/projects" element={<Projects />} /> */}
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>

      <Footer />

      <QuoteModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />

      <ChatAssistant isOpen={isChatOpen} setIsOpen={setIsChatOpen} />

    </>
  );
}

export default App;