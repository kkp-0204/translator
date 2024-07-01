
const historyLabel = document.querySelector('label[for="m-history"]');

historyLabel.addEventListener('click', () => {
  setTimeout(() => {
    window.location.href = 'New folder/translations.txt'; // replace with your text file URL
  }, 500); // wait for 2 seconds
});

const microphoneLabel = document.querySelector('label[for="m-microphone"]');

microphoneLabel.addEventListener('click', () => {
  setTimeout(() => {
    window.location.href = 'http://127.0.0.1:5000'; // replace with your text file URL
  }, 500); // wait for 2 seconds
});
const favoritesLabel = document.querySelector('label[for="m-favorites"]');

favoritesLabel.addEventListener('click', () => {
  setTimeout(() => {
    window.location.href = './rate_us.html'; // replace with your text file URL
  }, 500); // wait for 2 seconds
});
const profileLabel = document.querySelector('label[for="m-profile"]');

profileLabel.addEventListener('click', () => {
  setTimeout(() => {
    window.location.href = "contact_us.html"; // replace with your text file URL
  }, 500); // wait for 2 seconds
});