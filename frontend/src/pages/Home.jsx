import Hero from "../components/Hero";
import ServicesSection from "../components/ServicesSection";
import AboutSnapshot from "../components/AboutSnapshot";

export default function Home({ onOpenModal }) {
  return (
    <>
      <Hero onOpenModal={onOpenModal} />
      <AboutSnapshot />
      <ServicesSection />
    </>
  );
}
