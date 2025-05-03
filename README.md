# 📚 Slide-Extractor

> 🎥 Extract clean, study-ready slides from any YouTube lecture video and save them as a single, high-quality PDF.

**Slide-Extractor** is a Python tool that automatically detects and extracts unique slides from educational YouTube videos using perceptual hashing, and compiles them into a compressed, navigable PDF file. Ideal for students, educators, and self-learners.



## 🧠 Why Use Slide-Extractor?

- ✅ Saves time taking notes manually
- 🧠 Great for archiving video lectures into document form
- 🎯 Captures only **distinct** slides — skips near-duplicates
- 📄 Outputs a lightweight PDF that’s easy to share and store



## 🚀 Features

| Feature                     | Description                                            |
|----------------------------|--------------------------------------------------------|
| 🎥 YouTube Video Support    | Downloads videos directly using `pytube`               |
| 🖼️ Slide Detection          | Uses `imagehash` to detect visual slide changes        |
| 🧾 PDF Generation           | Saves all slides into a **single PDF** using `Pillow` |
| ⚙️ Configurable             | Adjust interval time and hash sensitivity              |
| 🧼 Clean Output             | Temporary data is removed, output is tidy              |



## 🧰 Requirements

Install the required Python libraries using:

```bash
pip install pytube opencv-python imagehash Pillow
```

#### ✅ Compatible with Python 3.10+



## 🧠 Behind the Scenes
Slide-Extractor samples video frames at regular time intervals and compares them using perceptual hashing. If a frame is sufficiently different from the previous one, it’s considered a new slide. These are then compiled into a compact PDF — perfect for review and offline access.


## 🙌 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.


## 🤝 Credits
+  [Pytube](https://github.com/pytube/pytube) for video downloading
+  [OpenCV](https://opencv.org/) for video frame processing
+  [ImageHash](https://github.com/JohannesBuchner/imagehash) for perceptual image comparison
+  [Pillow](https://python-pillow.org/) for image-to-PDF conversion

> "From video to notes — effortlessly." 📖
