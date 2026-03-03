// ===== SAFE SELECTORS =====
const content = document.querySelector(".content");
const sections = document.querySelectorAll(".section");
const navLinks = document.querySelectorAll(".nav-link");
const glow = document.querySelector(".cursor-glow");

// ===== DEBUG CHECK =====
console.log("content:", content);
console.log("sections:", sections.length);
console.log("navLinks:", navLinks.length);
console.log("glow:", glow);


// ===== SCROLL HIGHLIGHT (FOR SIDEBAR LAYOUT) =====



content.addEventListener("scroll", () => {
  let current = "";

  const scrollPosition = content.scrollTop + content.clientHeight / 2;

  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionBottom = sectionTop + section.clientHeight;

    if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
      current = section.getAttribute("id");
    }
  });

  navLinks.forEach(link => {
    link.classList.remove("active");

    if (link.getAttribute("href") === "#" + current) {
      link.classList.add("active");
    }
  });
});

// ===== CURSOR GLOW =====
if (glow) {
  document.addEventListener("mousemove", (e) => {
    glow.style.left = e.clientX + "px";
    glow.style.top = e.clientY + "px";
  });
}