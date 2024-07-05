# Text Summarizer Chrome Extension

This Chrome extension utilizes Natural Language Processing (NLP) to summarize text. It communicates with a Python server to perform text summarization using NLTK (Natural Language Toolkit) logic.

## Features

- Summarize text with a click of a button.
- NLP-based summarization using NLTK.
- Communicates with a Python server for text processing.

## Getting Started

1. **Setup Python Server:**
   - Clone the repository: `git clone https://github.com/TanishaPanigrahi/Text-Summarizer-Extension.git`
   - `mkdir root`
   - Add all the files in the folder root
   - Run the server: `python app.py`

2. **Install the Chrome Extension:**
   - Open Chrome and go to `chrome://extensions/`.
   - Enable "Developer mode" in the top right.
   - Click "Load unpacked" and select the `root` directory from this repository.

3. **Usage:**
   - Visit a webpage or open a new tab.
   - Enter the text you want to summarize in the input field.
   - Click the "Summarize" button.

4. **View Summarized Text:**
   - The summarized text will be displayed in the output section with a heading.

## Contributing

Feel free to contribute to the development of this Chrome extension. If you find any issues or have suggestions, please open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
