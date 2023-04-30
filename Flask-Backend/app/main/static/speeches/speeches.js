const tabs = document.querySelectorAll('[data-tabs]');
const container = document.querySelector('.container ul');

// Fetch content for selected tab
const fetchContent = async (tab) => {
  container.innerHTML = '';
  try {
    const response = await fetch(`/api/${tab}`);
    const data = await response.json();
    data.forEach((item) => {
      const li = document.createElement('li');
      if (tab === 'script') {
        li.innerText = item.script;
      } else if (tab === 'audio') {
        const audio = document.createElement('audio');
        audio.setAttribute('controls', '');
        const source = document.createElement('source');
        source.setAttribute('src', item.audio);
        audio.appendChild(source);
        li.appendChild(audio);
      } else if (tab === 'video') {
        const video = document.createElement('video');
        video.setAttribute('controls', '');
        const source = document.createElement('source');
        source.setAttribute('src', item.video);
        video.appendChild(source);
        li.appendChild(video);
      }
      container.appendChild(li);
    });
  } catch (error) {
    console.error(error);
  }
};

// Add click event listener to tabs
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    // Remove active class from all tabs
    tabs.forEach((tab) => tab.classList.remove('active'));
    // Add active class to selected tab
    tab.classList.add('active');
    // Fetch content for selected tab
    const selectedTab = tab.getAttribute('data-tabs');
    fetchContent(selectedTab);
  });
});

// Fetch content for default active tab on page load
const activeTab = document.querySelector('[data-tabs].active');
fetchContent(activeTab.getAttribute('data-tabs'));
