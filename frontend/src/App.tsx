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
import alternexLogo from "./assets/alternex-logo.jpg";
import ninjaNotesLogo from "./assets/WhatsApp Image 2025-06-24 at 14.20.44_a2706619.jpg";
import "./assets/airstrike/airstrike.ttf";

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

  const API_BASE = import.meta.env.PROD
    ? "/.netlify/functions" // Use Netlify Functions in production
    : "/api";

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
      const response = await fetch(`${API_BASE}/generate-notes`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: youtubeUrl,
          style: "comprehensive",
        }),
      });

      if (response.ok) {
        const data = await response.json();

        if (data.success) {
          setGeneratedNotes({
            content: data.notes,
            videoTitle: data.title || "Generated Notes",
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
      setError(
        error instanceof Error ? error.message : "Failed to connect to server"
      );
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
      const response = await fetch(`${API_BASE}/generate-pdf`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          notes: generatedNotes.content,
          title: generatedNotes.videoTitle || "Generated Notes",
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${generatedNotes.videoTitle || "notes"}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        return;
      } else {
        const errorText = await response.text();
        throw new Error(
          `PDF generation failed: ${response.status} - ${errorText}`
        );
      }
    } catch (error) {
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
            <div className="flex items-center space-x-4">
              {/* Logo and Brand */}
              <img
                src={ninjaNotesLogo}
                alt="NinjaNotes Logo"
                className="h-14 w-14 rounded-full object-cover shadow-lg"
              />
              <div className="flex flex-col justify-center">
                <span className="text-2xl font-extrabold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent tracking-wide drop-shadow-lg">
                  NinjaNotes
                </span>
                <span className="text-xs text-gray-400 mt-1 text-left">
                  Built by Sibsankar
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
      <section className="relative overflow-hidden hero-bg-animated min-h-screen flex items-center">
        {/* Simple Background */}
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>

        {/* Floating Elements - Hidden on mobile for better performance */}
        <div className="hidden md:block floating-element top-10 left-10">
          <div className="w-16 h-16 bg-purple-500/5 rounded-full border border-purple-500/10 flex items-center justify-center">
            <FileText className="w-6 h-6 text-purple-400" />
          </div>
        </div>
        <div className="hidden md:block floating-element top-20 right-15">
          <div className="w-12 h-12 bg-blue-500/5 rounded-full border border-blue-500/10 flex items-center justify-center">
            <Play className="w-4 h-4 text-blue-400" />
          </div>
        </div>
        <div className="hidden md:block floating-element bottom-20 left-20">
          <div className="w-20 h-20 bg-purple-500/5 rounded-full border border-purple-500/10 flex items-center justify-center">
            <BookOpen className="w-7 h-7 text-purple-400" />
          </div>
        </div>
        <div className="hidden md:block floating-element bottom-30 right-10">
          <div className="w-14 h-14 bg-cyan-500/5 rounded-full border border-cyan-500/10 flex items-center justify-center">
            <Download className="w-5 h-5 text-cyan-400" />
          </div>
        </div>

        {/* Additional Floating Elements - Hidden on mobile */}
        <div className="hidden lg:block floating-element top-1/3 left-1/6">
          <div className="w-10 h-10 bg-green-500/5 rounded-full border border-green-500/10 flex items-center justify-center">
            <Check className="w-4 h-4 text-green-400" />
          </div>
        </div>
        <div className="hidden lg:block floating-element top-2/3 right-1/4">
          <div className="w-8 h-8 bg-pink-500/5 rounded-full border border-pink-500/10 flex items-center justify-center">
            <Sparkles className="w-3 h-3 text-pink-400" />
          </div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-32 w-full">
          <div className="text-center">
            {/* Animated Badge */}
            <div className="inline-flex items-center px-4 sm:px-6 py-2 sm:py-3 bg-gray-800/60 backdrop-blur-sm rounded-full text-xs sm:text-sm text-purple-300 font-medium mb-6 sm:mb-8 border border-purple-500/30 animate-bounce-in hover-lift">
              <Sparkles className="w-3 h-3 sm:w-4 sm:h-4 mr-2 animate-sparkle" />
              AI-Powered Note Generation
              <div className="ml-2 w-1.5 h-1.5 sm:w-2 sm:h-2 bg-purple-400 rounded-full animate-pulse"></div>
            </div>

            {/* Animated Title */}
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4 sm:mb-6 leading-tight animate-fade-in-up px-2">
              Turn YouTube lectures into
              <span className="block gradient-text-animated mt-1 sm:mt-2">
                clear, downloadable notes
              </span>
            </h1>

            {/* Animated Description */}
            <p className="text-base sm:text-lg md:text-xl text-gray-300 mb-8 sm:mb-12 max-w-3xl mx-auto leading-relaxed animate-slide-in-left px-4">
              Transform any educational YouTube video (English, Hindi, and more)
              into organized, comprehensive study notes with our AI-powered.
            </p>

            {/* Main Form with Enhanced Animations */}
            {!showResults && (
              <div className="max-w-2xl mx-auto animate-slide-in-right px-4">
                <form onSubmit={handleSubmit}>
                  <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 p-2 bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-2xl border border-gray-700 hover-lift hover-glow">
                    <div className="flex-1 relative">
                      <Youtube className="absolute left-3 sm:left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 sm:w-5 sm:h-5 animate-wave" />
                      <input
                        type="url"
                        value={youtubeUrl}
                        onChange={(e) => setYoutubeUrl(e.target.value)}
                        placeholder="Paste YouTube video URL here..."
                        className="w-full pl-10 sm:pl-12 pr-3 sm:pr-4 py-3 sm:py-4 bg-transparent border-0 focus:outline-none focus:ring-0 text-white placeholder-gray-400 text-base sm:text-lg transition-all duration-300 focus:placeholder-gray-500"
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={isProcessing}
                      className="px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-xl transition-all duration-300 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:-translate-y-1 disabled:transform-none hover-glow animate-bounce-in text-sm sm:text-base"
                    >
                      {isProcessing ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 sm:h-5 sm:w-5 border-2 border-white border-t-transparent"></div>
                          <span>Processing...</span>
                        </>
                      ) : (
                        <>
                          <span>Generate Notes</span>
                          <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5 animate-wave" />
                        </>
                      )}
                    </button>
                  </div>
                </form>

                {error && (
                  <div className="mt-4 p-3 sm:p-4 bg-red-900/50 border border-red-500/50 rounded-lg text-red-300 text-center animate-bounce-in text-sm sm:text-base">
                    {error}
                  </div>
                )}

                <p className="text-xs sm:text-sm text-gray-400 mt-4 animate-fade-in-up px-4">
                  Free forever • No registration required • Export to PDF
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Animated Scroll Indicator - Hidden on mobile */}
        <div className="hidden md:block absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-gray-400 rounded-full flex justify-center">
            <div className="w-1 h-3 bg-gray-400 rounded-full mt-2 animate-pulse"></div>
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
        className="py-24 bg-gradient-to-br from-gray-800 to-gray-900 relative overflow-hidden"
      >
        {/* Animated background elements */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-32 h-32 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full blur-3xl animate-pulse"></div>
          <div
            className="absolute bottom-10 right-10 w-40 h-40 bg-gradient-to-br from-cyan-500 to-purple-500 rounded-full blur-3xl animate-pulse"
            style={{ animationDelay: "2s" }}
          ></div>
          <div
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-gradient-to-br from-pink-500 to-orange-500 rounded-full blur-2xl animate-pulse"
            style={{ animationDelay: "4s" }}
          ></div>
        </div>

        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="bg-gray-900/80 backdrop-blur-sm rounded-3xl p-12 border border-gray-700 shadow-2xl">
            {/* Built by Alternex Badge */}
            <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-600/20 to-blue-600/20 backdrop-blur-sm rounded-full text-sm text-purple-300 font-medium mb-8 border border-purple-500/30 animate-bounce-in">
              <span className="mr-2 animate-sparkle">🚀</span>
              Get Set Groww
            </div>

            {/* Company Logo and Name */}
            <div className="flex items-center justify-center space-x-4 group mb-8">
              {/* Simplified Logo */}
              <div className="w-20 h-20 bg-gray-800 p-2 rounded-2xl shadow-lg transition-all duration-300 group-hover:scale-110 group-hover:shadow-purple-500/20">
                <img
                  src={alternexLogo}
                  alt="Alternex Logo"
                  className="w-full h-full object-contain"
                />
              </div>

              {/* Simplified Company Name */}
              <div className="text-left">
                <h2
                  className="text-5xl font-orbitron font-bold text-gray-200 tracking-wider airstrike-font"
                  style={{ textShadow: "0 2px 10px rgba(192, 132, 252, 0.2)" }}
                >
                  Alternex
                </h2>
              </div>
            </div>

            {/* Company Description and Tagline */}
            <div className="max-w-3xl mx-auto space-y-6 mb-8">
              <p className="text-xl text-gray-300 leading-relaxed animate-fade-in-up">
                Revolutionizing e-learning through intelligent tools and
                seamless digital experiences. Creating innovative educational
                tools that bridge technology and learning. Focused on
                personalized, high-quality content and user-first experiences.
              </p>
              <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-full border border-purple-500/20">
                <span className="text-purple-300 font-medium text-lg">
                  ✨ Upgrading E-Learning With AI
                </span>
              </div>
            </div>

            {/* Social Media Handles */}
            <div className="flex flex-wrap justify-center gap-4 mb-8">
              <a
                href="https://www.instagram.com/alternex_/"
                target="_blank"
                rel="noopener noreferrer"
                className="group relative overflow-hidden px-6 py-3 bg-gradient-to-r from-pink-500 via-purple-600 to-pink-600 rounded-xl transition-all duration-500 transform hover:-translate-y-1 hover:shadow-xl hover:shadow-pink-500/30"
              >
                {/* Animated background */}
                <div className="absolute inset-0 bg-gradient-to-r from-pink-600 via-purple-700 to-pink-700 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                {/* Content */}
                <div className="relative flex items-center space-x-2">
                  <div className="w-5 h-5 bg-white/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
                    <Instagram className="w-3 h-3 text-white" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-white font-semibold text-sm">
                      Alternex
                    </span>
                    <span className="text-pink-100 text-xs font-medium">
                      Follow us
                    </span>
                  </div>
                </div>

                {/* Hover effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
              </a>

              <a
                href="https://chat.whatsapp.com/Hhx44w11K7J6qnnAuQ0f9z?mode=ac_t"
                target="_blank"
                rel="noopener noreferrer"
                className="group relative overflow-hidden px-6 py-3 bg-gradient-to-r from-green-500 via-emerald-600 to-green-600 rounded-xl transition-all duration-500 transform hover:-translate-y-1 hover:shadow-xl hover:shadow-green-500/30"
              >
                {/* Animated background */}
                <div className="absolute inset-0 bg-gradient-to-r from-green-600 via-emerald-700 to-green-700 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                {/* Content */}
                <div className="relative flex items-center space-x-2">
                  <div className="w-5 h-5 bg-white/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
                    <div className="w-3 h-3 text-white">
                      <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.488" />
                      </svg>
                    </div>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-white font-semibold text-sm">
                      WhatsApp
                    </span>
                    <span className="text-green-100 text-xs font-medium">
                      Chat with us
                    </span>
                  </div>
                </div>

                {/* Hover effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
              </a>

              <a
                href="https://www.linkedin.com/company/alternex/"
                target="_blank"
                rel="noopener noreferrer"
                className="group relative overflow-hidden px-6 py-3 bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 rounded-xl transition-all duration-500 transform hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/30"
              >
                {/* Animated background */}
                <div className="absolute inset-0 bg-gradient-to-r from-blue-700 via-blue-800 to-blue-900 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                {/* Content */}
                <div className="relative flex items-center space-x-2">
                  <div className="w-5 h-5 bg-white/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
                    <Linkedin className="w-3 h-3 text-white" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-white font-semibold text-sm">
                      LinkedIn
                    </span>
                    <span className="text-blue-100 text-xs font-medium">
                      Connect with us
                    </span>
                  </div>
                </div>

                {/* Hover effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
              </a>

              <a
                href="mailto:alternex5@gmail.com"
                className="group relative overflow-hidden px-6 py-3 bg-gradient-to-r from-red-500 via-red-600 to-red-700 rounded-xl transition-all duration-500 transform hover:-translate-y-1 hover:shadow-xl hover:shadow-red-500/30"
              >
                {/* Animated background */}
                <div className="absolute inset-0 bg-gradient-to-r from-red-600 via-red-700 to-red-800 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                {/* Content */}
                <div className="relative flex items-center space-x-2">
                  <div className="w-5 h-5 bg-white/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
                    <Mail className="w-3 h-3 text-white" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-white font-semibold text-sm">
                      Gmail
                    </span>
                    <span className="text-red-100 text-xs font-medium">
                      Email us
                    </span>
                  </div>
                </div>

                {/* Hover effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
              </a>
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
      <footer
        id="contact"
        className="bg-black text-white py-16 relative overflow-hidden"
      >
        {/* Animated background elements */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-32 h-32 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full blur-3xl animate-pulse"></div>
          <div
            className="absolute bottom-10 right-10 w-40 h-40 bg-gradient-to-br from-cyan-500 to-purple-500 rounded-full blur-3xl animate-pulse"
            style={{ animationDelay: "2s" }}
          ></div>
          <div
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-gradient-to-br from-pink-500 to-orange-500 rounded-full blur-2xl animate-pulse"
            style={{ animationDelay: "4s" }}
          ></div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          {/* Footer Content */}
          <div className="grid md:grid-cols-4 gap-8">
            <div className="md:col-span-2">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-white" />
                </div>
                <div className="flex flex-col">
                  <span className="text-xl font-bold">NinjaNotes</span>
                  <span className="text-xs text-gray-400 -mt-1">
                    powered by Alternex
                  </span>
                </div>
              </div>
              <p className="text-gray-400 mb-6 max-w-md">
                Transform YouTube educational videos into comprehensive study
                notes with AI-powered technology. Free, fast, and reliable.
              </p>
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
                    Built by Alternex
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Connect</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <a
                    href="https://instagram.com/alternex"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors"
                  >
                    Instagram
                  </a>
                </li>
                <li>
                  <a
                    href="https://linkedin.com/company/alternex"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors"
                  >
                    LinkedIn
                  </a>
                </li>
                <li>
                  <a
                    href="https://youtube.com/@alternex"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors"
                  >
                    YouTube
                  </a>
                </li>
                <li>
                  <a
                    href="mailto:hello@alternex.com"
                    className="hover:text-white transition-colors"
                  >
                    Email
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>
              &copy; 2025 NinjaNotes. Built by{" "}
              <span className="text-purple-400 font-medium">Sibsankar</span>.
              All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
