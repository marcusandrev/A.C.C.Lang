document.addEventListener('DOMContentLoaded', function () {
  const editor = document.querySelector('.editor');
  const lineNumbers = document.querySelector('.line-numbers');
  const themeSwitch = document.getElementById('theme-switch');
  const logo = document.getElementById('logo');
  const body = document.body;

  // Line numbers
  function updateLineNumbers() {
    const lineCount = editor.value.split('\n').length;
    lineNumbers.innerHTML = Array.from(
      { length: lineCount },
      (_, i) => i + 1
    ).join('<br>');
  }

  editor.addEventListener('input', updateLineNumbers);
  editor.addEventListener('scroll', () => {
    lineNumbers.scrollTop = editor.scrollTop;
  });

  // Theme switch
  themeSwitch.addEventListener('change', () => {
    logo.src = themeSwitch.checked
      ? '/static/assets/logo-light.png'
      : '/static/assets/logo-dark.png';
    body.classList.toggle('dark-mode', themeSwitch.checked);
  });

  // Replace all curly quotes with straight quotes
  editor.addEventListener('input', function () {
    this.value = this.value.replace(/“|”/g, '"');
  });

  // Tab key
  editor.addEventListener('keydown', function (event) {
    if (event.key === 'Tab') {
      event.preventDefault();
      const start = this.selectionStart;
      const end = this.selectionEnd;
      const spaces = '     ';
      this.value =
        this.value.substring(0, start) + spaces + this.value.substring(end);
      this.selectionStart = this.selectionEnd = start + spaces.length;
    }
  });

  updateLineNumbers();
});
