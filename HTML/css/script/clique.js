document.querySelectorAll('aside ul li img').forEach((img, index) => {
  img.addEventListener('click', () => {
    // Substitua os links abaixo pelos destinos desejados
    const links = [
      'pagina-roupas.html', // Link para "Roupas"
      'pagina-moveis.html', // Link para "Móveis"
      'pagina-alimentos.html', // Link para "Alimentos"
      'pagina-brinquedos.html' // Link para "Brinquedos"
    ];
    window.location.href = links[index];
  });
});
