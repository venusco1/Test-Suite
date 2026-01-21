console.log("Test Suite Manager UI Loaded");


const toolPanel = document.getElementById('toolPanel');
const toolCollapseBtn = document.getElementById('toolCollapseBtn');
const toolExpandBtn = document.getElementById('toolExpandBtn');

toolCollapseBtn.addEventListener('click', (e) => {
    e.preventDefault();
    toolPanel.classList.add('panel-collapsed');
    toolExpandBtn.style.display = 'block';
});

toolExpandBtn.addEventListener('click', () => {
    toolPanel.classList.remove('panel-collapsed');
    toolExpandBtn.style.display = 'none';
});


// Additional JS for editor functionality can be added here

