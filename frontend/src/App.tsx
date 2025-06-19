import React, { useState } from "react";
import {
  Youtube,
  FileText,
  Download,
  Sparkles,
  Play,
  ArrowRight,
  Check,
  Github,
  Mail,
  Shield,
  BookOpen,
  Clock,
  User,
  Calendar,
  ExternalLink,
  Instagram,
  Linkedin,
  Twitter,
} from "lucide-react";
import ReactMarkdown from "react-markdown";

interface GeneratedNotes {
  content: string;
  videoTitle?: string;
  videoDuration?: string;
  videoAuthor?: string;
  publishDate?: string;
}

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [generatedNotes, setGeneratedNotes] = useState<GeneratedNotes | null>(
    null
  );
  const [showResults, setShowResults] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPopup, setShowPopup] = useState(false);

  const validateYouTubeUrl = (url: string) => {
    const youtubeRegex =
      /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]+/;
    return youtubeRegex.test(url);
  };

  const generateNotes = async () => {
    if (!youtubeUrl.trim()) {
      setError("Please enter a YouTube URL");
      return;
    }

    if (!validateYouTubeUrl(youtubeUrl)) {
      setError("Please enter a valid YouTube URL");
      return;
    }

    setIsProcessing(true);
    setShowResults(false);
    setError(null);

    try {
      const response = await fetch("/api/generate-notes/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: youtubeUrl,
        }),
      });

      if (response.ok) {
        const data = await response.json();

        if (data.success) {
          setGeneratedNotes({
            content: data.notes,
            videoTitle: data.video_title || data.title,
            videoDuration: data.video_duration || data.duration,
            videoAuthor: data.video_author || data.author,
            publishDate: data.publish_date || data.date,
          });

          setShowResults(true);
          setIsProcessing(false);
          setShowPopup(true);
          setTimeout(() => setShowPopup(false), 2000); // Auto-dismiss after 2s
          return;
        } else {
          throw new Error(data.error || "Failed to generate notes");
        }
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error("API Error:", error);

      // Handle different types of errors with better messages
      let errorMessage = "Failed to connect to server";

      if (error instanceof Error) {
        if (error.message.includes("404")) {
          errorMessage =
            "No transcript available for this video. Please try a different video with subtitles enabled.";
        } else if (error.message.includes("403")) {
          errorMessage =
            "Transcripts are disabled for this video. The video owner has disabled subtitle generation.";
        } else if (error.message.includes("500")) {
          errorMessage = "Server error occurred. Please try again later.";
        } else if (error.message.includes("Failed to fetch transcript")) {
          errorMessage =
            "Failed to fetch transcript. This might be due to language restrictions or video settings.";
        } else if (error.message.includes("No transcript available")) {
          errorMessage =
            "No transcript available for this video. Please try a different video with subtitles enabled.";
        } else {
          errorMessage = error.message;
        }
      }

      setError(errorMessage);
      setIsProcessing(false);
      return;
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    generateNotes();
  };

  const downloadPDF = async () => {
    if (!generatedNotes) return;

    try {
      console.log("📄 Generating PDF...");
      const response = await fetch("/api/download-pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          notes: generatedNotes.content,
          title: generatedNotes.videoTitle || "Generated Notes",
          youtube_url: youtubeUrl,
        }),
      });

      if (response.ok) {
        // Create blob and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${generatedNotes.videoTitle || "notes"}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        console.log("✅ PDF downloaded successfully!");
        return;
      } else {
        const errorText = await response.text();
        console.error("❌ PDF generation failed:", response.status, errorText);
        throw new Error(
          `PDF generation failed: ${response.status} - ${errorText}`
        );
      }
    } catch (error) {
      console.error("❌ PDF download error:", error);
      alert(
        `PDF download failed: ${
          error instanceof Error ? error.message : "Unknown error"
        }. Please try again or copy the notes manually.`
      );
    }
  };

  const generateNewNotes = () => {
    setShowResults(false);
    setGeneratedNotes(null);
    setYoutubeUrl("");
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Popup Animation for Notes Generated */}
      {showPopup && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="bg-gradient-to-br from-purple-600 to-blue-600 text-white px-8 py-6 rounded-2xl shadow-2xl animate-popup-scale">
            <div className="flex flex-col items-center">
              <Sparkles className="w-10 h-10 mb-2 animate-bounce" />
              <span className="text-2xl font-bold mb-1">Notes Generated!</span>
              <span className="text-base text-blue-100">
                Scroll down to view your beautiful notes 🎉
              </span>
            </div>
          </div>
        </div>
      )}
      {/* Header */}
      <header className="relative z-10 bg-gray-900/80 backdrop-blur-md border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                  AutoNoteGen
                </span>
                <span className="text-xs text-gray-400 -mt-1">
                  built by sibsankar
                </span>
              </div>
            </div>
            <nav className="hidden md:flex items-center space-x-8">
              <a
                href="#features"
                className="text-gray-300 hover:text-white transition-colors"
              >
                Features
              </a>
              <a
                href="#how-it-works"
                className="text-gray-300 hover:text-white transition-colors"
              >
                How It Works
              </a>
              <a
                href="#creator"
                className="text-gray-300 hover:text-white transition-colors"
              >
                Creator
              </a>
              <a
                href="#contact"
                className="text-gray-300 hover:text-white transition-colors"
              >
                Contact
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-gray-900 via-purple-900/20 to-blue-900/20">
        <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 bg-gray-800/60 backdrop-blur-sm rounded-full text-sm text-purple-300 font-medium mb-8 border border-purple-500/30">
              <Sparkles className="w-4 h-4 mr-2" />
              AI-Powered Note Generation
            </div>

            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
              Turn YouTube lectures into
              <span className="block bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                clear, downloadable notes
              </span>
            </h1>

            <p className="text-xl text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
              Transform any educational YouTube video (English, Hindi, and more)
              into organized, comprehensive study notes with our AI-powered
              tool. Perfect for students, researchers, and lifelong learners
              worldwide.
            </p>

            {/* Main Form */}
            {!showResults && (
              <div className="max-w-2xl mx-auto">
                <form onSubmit={handleSubmit}>
                  <div className="flex flex-col sm:flex-row gap-4 p-2 bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-2xl border border-gray-700">
                    <div className="flex-1 relative">
                      <Youtube className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                      <input
                        type="url"
                        value={youtubeUrl}
                        onChange={(e) => setYoutubeUrl(e.target.value)}
                        placeholder="Paste YouTube video URL here..."
                        className="w-full pl-12 pr-4 py-4 bg-transparent border-0 focus:outline-none focus:ring-0 text-white placeholder-gray-400 text-lg"
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={isProcessing}
                      className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-xl transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:transform-none"
                    >
                      {isProcessing ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                          <span>Processing...</span>
                        </>
                      ) : (
                        <>
                          <span>Generate Notes</span>
                          <ArrowRight className="w-5 h-5" />
                        </>
                      )}
                    </button>
                  </div>
                </form>

                {error && (
                  <div className="mt-4 p-4 bg-red-900/50 border border-red-500/50 rounded-lg text-red-300 text-center">
                    {error}
                  </div>
                )}

                <p className="text-sm text-gray-400 mt-4">
                  Free forever • No registration required • Export to PDF
                </p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Results Section */}
      {showResults && generatedNotes && (
        <section className="py-16 bg-gray-800">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Video Info Header */}
            <div className="bg-gray-900/80 backdrop-blur-sm rounded-2xl p-8 mb-8 border border-gray-700">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
                <div className="flex-1">
                  {/* Only show title if not 'Unknown Title' */}
                  {generatedNotes.videoTitle &&
                    generatedNotes.videoTitle !== "Unknown Title" && (
                      <h2 className="text-3xl lg:text-4xl font-extrabold text-white mb-4">
                        {generatedNotes.videoTitle}
                      </h2>
                    )}
                  {/* Only show author if not 'Unknown Author' */}
                  {(generatedNotes.videoDuration ||
                    (generatedNotes.videoAuthor &&
                      generatedNotes.videoAuthor !== "Unknown Author") ||
                    generatedNotes.publishDate) && (
                    <div className="flex flex-wrap items-center gap-6 text-gray-300">
                      {generatedNotes.videoDuration && (
                        <div className="flex items-center space-x-2">
                          <Clock className="w-4 h-4" />
                          <span>{generatedNotes.videoDuration}</span>
                        </div>
                      )}
                      {generatedNotes.videoAuthor &&
                        generatedNotes.videoAuthor !== "Unknown Author" && (
                          <div className="flex items-center space-x-2">
                            <User className="w-4 h-4" />
                            <span>{generatedNotes.videoAuthor}</span>
                          </div>
                        )}
                      {generatedNotes.publishDate && (
                        <div className="flex items-center space-x-2">
                          <Calendar className="w-4 h-4" />
                          <span>{generatedNotes.publishDate}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
                <div className="flex flex-col sm:flex-row gap-4">
                  <button
                    onClick={downloadPDF}
                    className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-semibold rounded-xl transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                  >
                    <Download className="w-5 h-5" />
                    <span>Download PDF</span>
                  </button>
                  <button
                    onClick={generateNewNotes}
                    className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-xl transition-all duration-200 flex items-center justify-center space-x-2"
                  >
                    <Youtube className="w-5 h-5" />
                    <span>New Video</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Generated Notes Display */}
            <div className="bg-gray-900/60 backdrop-blur-sm rounded-xl p-8 border border-gray-700">
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
                <FileText className="w-5 h-5 mr-2 text-blue-400" />
                Generated Notes
              </h3>
              <div className="prose prose-invert prose-lg max-w-none">
                <ReactMarkdown
                  components={{
                    h1: ({ node, ...props }: { node: any }) => (
                      <h1
                        className="text-3xl font-extrabold text-white mt-8 mb-4"
                        {...props}
                      />
                    ),
                    h2: ({ node, ...props }: { node: any }) => (
                      <h2
                        className="text-2xl font-bold text-white mt-6 mb-3"
                        {...props}
                      />
                    ),
                    h3: ({ node, ...props }: { node: any }) => (
                      <h3
                        className="text-xl font-semibold text-white mt-4 mb-2"
                        {...props}
                      />
                    ),
                    ul: ({ node, ...props }: { node: any }) => (
                      <ul className="list-disc pl-6 mb-4" {...props} />
                    ),
                    ol: ({ node, ...props }: { node: any }) => (
                      <ol className="list-decimal pl-6 mb-4" {...props} />
                    ),
                    li: ({ node, ...props }: { node: any }) => (
                      <li className="mb-1" {...props} />
                    ),
                    strong: ({ node, ...props }: { node: any }) => (
                      <strong className="font-bold text-blue-300" {...props} />
                    ),
                    p: ({ node, ...props }: { node: any }) => (
                      <p className="mb-3" {...props} />
                    ),
                    code: ({ node, ...props }: { node: any }) => (
                      <code
                        className="bg-gray-800 px-2 py-1 rounded text-white font-mono"
                        {...props}
                      />
                    ),
                    pre: ({ node, ...props }: { node: any }) => (
                      <pre
                        className="bg-gray-800 rounded-lg p-4 overflow-x-auto mb-4 text-white"
                        {...props}
                      />
                    ),
                  }}
                  skipHtml
                >
                  {generatedNotes.content}
                </ReactMarkdown>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-8 text-center">
              <div className="inline-flex flex-col sm:flex-row gap-4 p-4 bg-gray-900/60 backdrop-blur-sm rounded-xl border border-gray-700">
                <button
                  onClick={downloadPDF}
                  className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-semibold rounded-xl transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                >
                  <Download className="w-5 h-5" />
                  <span>Download Complete Notes as PDF</span>
                </button>
                <a
                  href={youtubeUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-xl transition-all duration-200 flex items-center justify-center space-x-2"
                >
                  <ExternalLink className="w-5 h-5" />
                  <span>View Original Video</span>
                </a>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Features Section - Only show when not displaying results */}
      {!showResults && (
        <section id="features" className="py-24 bg-gray-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                Why Choose AutoNoteGen?
              </h2>
              <p className="text-xl text-gray-300 max-w-2xl mx-auto">
                The most efficient way to extract knowledge from educational
                videos
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              <div className="text-center group hover:transform hover:-translate-y-2 transition-all duration-300">
                <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:shadow-xl group-hover:shadow-green-500/25">
                  <Check className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  100% Free
                </h3>
                <p className="text-gray-300">
                  No hidden costs, no subscriptions. Generate unlimited notes
                  from YouTube videos completely free.
                </p>
              </div>

              <div className="text-center group hover:transform hover:-translate-y-2 transition-all duration-300">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:shadow-xl group-hover:shadow-blue-500/25">
                  <BookOpen className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  Multi-Language
                </h3>
                <p className="text-gray-300">
                  Supports English, Hindi, and other languages. Automatically
                  detects and processes content in the original language.
                </p>
              </div>

              <div className="text-center group hover:transform hover:-translate-y-2 transition-all duration-300">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:shadow-xl group-hover:shadow-purple-500/25">
                  <Download className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  One-Click PDF
                </h3>
                <p className="text-gray-300">
                  Download your notes instantly as a beautifully formatted PDF
                  ready for studying.
                </p>
              </div>

              <div className="text-center group hover:transform hover:-translate-y-2 transition-all duration-300">
                <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:shadow-xl group-hover:shadow-orange-500/25">
                  <Sparkles className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  AI-Powered
                </h3>
                <p className="text-gray-300">
                  Advanced AI technology summarizes key points and creates
                  structured, comprehensive notes.
                </p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* How It Works - Only show when not displaying results */}
      {!showResults && (
        <section
          id="how-it-works"
          className="py-24 bg-gradient-to-br from-gray-900 to-gray-800"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                How It Works
              </h2>
              <p className="text-xl text-gray-300 max-w-2xl mx-auto">
                Three simple steps to transform any YouTube video into
                comprehensive study notes
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
              <div className="text-center relative">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-600 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-purple-500/25">
                  <Youtube className="w-10 h-10 text-white" />
                </div>
                <div className="absolute top-10 right-0 hidden md:block">
                  <ArrowRight className="w-6 h-6 text-gray-600" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  1. Paste YouTube Link
                </h3>
                <p className="text-gray-300">
                  Simply copy and paste the URL of any educational YouTube video
                  into our input field.
                </p>
              </div>

              <div className="text-center relative">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-blue-500/25">
                  <Sparkles className="w-10 h-10 text-white" />
                </div>
                <div className="absolute top-10 right-0 hidden md:block">
                  <ArrowRight className="w-6 h-6 text-gray-600" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  2. AI Processing
                </h3>
                <p className="text-gray-300">
                  Our advanced AI analyzes the video content and extracts key
                  concepts, topics, and insights.
                </p>
              </div>

              <div className="text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-cyan-600 to-green-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-cyan-500/25">
                  <FileText className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  3. Download Notes
                </h3>
                <p className="text-gray-300">
                  Get your organized, comprehensive notes as a PDF file ready
                  for studying or sharing.
                </p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Creator Section */}
      <section
        id="creator"
        className="py-24 bg-gradient-to-br from-gray-800 to-gray-900"
      >
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-gray-900/80 backdrop-blur-sm rounded-3xl p-12 border border-gray-700 shadow-2xl">
            <div className="mb-8">
              <div className="w-24 h-24 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-purple-500/25">
                <User className="w-12 h-12 text-white" />
              </div>
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                Built by{" "}
                <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                  Sibsankar Samal
                </span>
              </h2>
              <p className="text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
                Passionate developer creating tools to make learning more
                accessible and efficient. Connect with me on social media to
                stay updated with my latest projects!
              </p>
            </div>

            <div className="flex flex-wrap justify-center gap-6">
              <a
                href="https://github.com/sibsankarsamal"
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center space-x-3 px-6 py-3 bg-gray-800 hover:bg-gray-700 rounded-xl transition-all duration-200 border border-gray-600 hover:border-gray-500 transform hover:-translate-y-1 hover:shadow-lg"
              >
                <Github className="w-5 h-5 text-gray-300 group-hover:text-white" />
                <span className="text-gray-300 group-hover:text-white font-medium">
                  GitHub
                </span>
              </a>

              <a
                href="https://linkedin.com/in/sibsankarsamal"
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center space-x-3 px-6 py-3 bg-blue-600 hover:bg-blue-500 rounded-xl transition-all duration-200 transform hover:-translate-y-1 hover:shadow-lg"
              >
                <Linkedin className="w-5 h-5 text-white" />
                <span className="text-white font-medium">LinkedIn</span>
              </a>

              <a
                href="https://twitter.com/sibsankarsamal"
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center space-x-3 px-6 py-3 bg-sky-500 hover:bg-sky-400 rounded-xl transition-all duration-200 transform hover:-translate-y-1 hover:shadow-lg"
              >
                <Twitter className="w-5 h-5 text-white" />
                <span className="text-white font-medium">Twitter</span>
              </a>

              <a
                href="https://instagram.com/sibsankarsamal"
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center space-x-3 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-400 hover:to-purple-500 rounded-xl transition-all duration-200 transform hover:-translate-y-1 hover:shadow-lg"
              >
                <Instagram className="w-5 h-5 text-white" />
                <span className="text-white font-medium">Instagram</span>
              </a>
            </div>

            <div className="mt-8 pt-8 border-t border-gray-700">
              <p className="text-gray-400 text-sm">
                💡 Have suggestions or found a bug? Feel free to reach out
                through any of the platforms above!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="py-16 bg-gray-800 border-t border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-8 text-gray-400">
              <div className="flex items-center space-x-2">
                <Shield className="w-5 h-5" />
                <span className="text-sm font-medium">Secure & Private</span>
              </div>
              <div className="flex items-center space-x-2">
                <Check className="w-5 h-5" />
                <span className="text-sm font-medium">Always Free</span>
              </div>
              <div className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5" />
                <span className="text-sm font-medium">AI-Powered</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="bg-black text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="md:col-span-2">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-white" />
                </div>
                <div className="flex flex-col">
                  <span className="text-xl font-bold">AutoNoteGen</span>
                  <span className="text-xs text-gray-400 -mt-1">
                    built by sibsankar
                  </span>
                </div>
              </div>
              <p className="text-gray-400 mb-6 max-w-md">
                Transform YouTube educational videos into comprehensive study
                notes with AI-powered technology. Free, fast, and reliable.
              </p>
              <div className="flex space-x-4">
                <a
                  href="https://github.com/sibsankarsamal"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <Github className="w-6 h-6" />
                </a>
                <a
                  href="https://linkedin.com/in/sibsankarsamal"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <Linkedin className="w-6 h-6" />
                </a>
                <a
                  href="https://twitter.com/sibsankarsamal"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <Twitter className="w-6 h-6" />
                </a>
                <a
                  href="https://instagram.com/sibsankarsamal"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <Instagram className="w-6 h-6" />
                </a>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <a
                    href="#features"
                    className="hover:text-white transition-colors"
                  >
                    Features
                  </a>
                </li>
                <li>
                  <a
                    href="#how-it-works"
                    className="hover:text-white transition-colors"
                  >
                    How It Works
                  </a>
                </li>
                <li>
                  <a
                    href="#creator"
                    className="hover:text-white transition-colors"
                  >
                    Creator
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Connect</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <a
                    href="https://github.com/sibsankarsamal"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors"
                  >
                    GitHub
                  </a>
                </li>
                <li>
                  <a
                    href="https://linkedin.com/in/sibsankarsamal"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors"
                  >
                    LinkedIn
                  </a>
                </li>
                <li>
                  <a
                    href="https://twitter.com/sibsankarsamal"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors"
                  >
                    Twitter
                  </a>
                </li>
                <li>
                  <a
                    href="https://instagram.com/sibsankarsamal"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors"
                  >
                    Instagram
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>
              &copy; 2025 AutoNoteGen. Built with ❤️ by Sibsankar Samal. All
              rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
