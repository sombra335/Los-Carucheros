// Galería con flechas  
document.addEventListener('DOMContentLoaded', () => {                                  // :contentReference[oaicite:7]{index=7}
  const images = ['images/img1.jpg', 'images/img2.jpg', 'images/img3.jpg'];            // Actualiza nombres
  let index = 0;
  const imgEl = document.getElementById('gallery-img');
  document.querySelector('.gallery-nav.prev').addEventListener('click', () => {
    index = (index - 1 + images.length) % images.length;
    imgEl.src = images[index];
  });
  document.querySelector('.gallery-nav.next').addEventListener('click', () => {
    index = (index + 1) % images.length;
    imgEl.src = images[index];
  });
});
