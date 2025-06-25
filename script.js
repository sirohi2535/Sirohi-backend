document.getElementById("videoForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = new FormData(this);

  const response = await fetch("https://radios-forecast-organ-guestbook.trycloudflare.com/generate-video", {
    method: "POST",
    body: form,
  });

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);

  const video = document.createElement("video");
  video.controls = true;
  video.src = url;
  document.body.appendChild(video);
});
