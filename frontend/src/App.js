import { useState, useRef, useEffect } from 'react';
import { Send, Scale, MessageCircle, User, Sparkles, ChevronDown } from 'lucide-react';

function App() {
  const [userMessage, setUserMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([
    {
      role: 'lawchecker',
      text: 'Hello! I am LawChecker, your legal assistant. How can I help you today?'
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [lawType, setLawType] = useState('');
  const [showModal, setShowModal] = useState(true);
  const [tempLawType, setTempLawType] = useState('un');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  const isGreek = (text) => /[Α-Ωα-ωίϊΐόάέύϋΰήώ]/.test(text);

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleModalConfirm = () => {
    setLawType(tempLawType);
    setShowModal(false);
  };

  const handleLawTypeChange = (newLawType) => {
    setLawType(newLawType);
    // Προαιρετικά: Μπορείς να προσθέσεις ένα μήνυμα στο chat ότι άλλαξε το jurisdiction
    setChatHistory(prev => [
      ...prev,
      {
        role: 'lawchecker',
        text: `✅ Jurisdiction updated to ${newLawType === 'un' ? 'United Nations' : 'Greece'}`
      }
    ]);
  };

  const handleSend = async () => {
    if (!userMessage.trim() || isLoading) return;

    const newMessage = userMessage.trim();
    setUserMessage('');

    const newHistory = [...chatHistory, { role: 'user', text: newMessage }];
    setChatHistory(newHistory);
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_message: newMessage, law_type: lawType })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      setChatHistory(prev => [
        ...prev,
        {
          role: 'lawchecker',
          text: data.response,
          sources: data.sources || [],
          showSources: false,
        }
      ]);
    } catch (error) {
      setChatHistory(prev => [
        ...prev,
        {
          role: 'lawchecker',
          text: '❌ An error occurred while communicating with the backend.'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQuestions = [
    'What is labor law?',
    'What are my rights?',
    'How do I write a contract?',
    'What do I do in case of a dispute?'
  ];

  const getLawTypeDisplay = () => {
    return lawType === 'un' ? 'United Nations' : 'Greece';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Modal Overlay */}
      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in">
          <div className="relative max-w-md w-full">
            {/* Modal Background Glow */}
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-3xl blur-2xl opacity-20"></div>
            
            {/* Modal Content */}
            <div className="relative backdrop-blur-xl bg-white/95 border border-white/30 rounded-3xl shadow-2xl shadow-blue-500/25 p-8 animate-fade-in">
              <div className="text-center mb-8">
                {/* Modal Icon */}
                <div className="relative mx-auto mb-6 w-16 h-16">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur-lg opacity-75"></div>
                  <div className="relative bg-gradient-to-r from-blue-600 to-indigo-600 p-4 rounded-2xl">
                    <Scale className="w-8 h-8 text-white" />
                  </div>
                </div>

                {/* Modal Title */}
                <h2 className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-3">
                  Welcome to LawChecker
                </h2>
                <p className="text-gray-600 font-medium">
                  Please select your preferred jurisdiction to get started
                </p>
              </div>

              {/* Law Type Selection */}
              <div className="space-y-4 mb-8">
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Choose Jurisdiction:
                </label>
                
                <div className="space-y-3">
                  <button
                    onClick={() => setTempLawType('un')}
                    className={`w-full p-4 rounded-2xl border-2 transition-all duration-300 text-left group ${
                      tempLawType === 'un'
                        ? 'border-blue-500 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-lg shadow-blue-500/20'
                        : 'border-gray-200 bg-white/50 hover:border-blue-300 hover:bg-blue-50/50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold text-gray-800 group-hover:text-blue-700 transition-colors">
                          🌍 United Nations
                        </h3>
                        <p className="text-sm text-gray-600 mt-1">
                          International law and regulations
                        </p>
                      </div>
                      {tempLawType === 'un' && (
                        <div className="w-5 h-5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center">
                          <div className="w-2 h-2 bg-white rounded-full"></div>
                        </div>
                      )}
                    </div>
                  </button>

                  <button
                    onClick={() => setTempLawType('greek')}
                    className={`w-full p-4 rounded-2xl border-2 transition-all duration-300 text-left group ${
                      tempLawType === 'greek'
                        ? 'border-blue-500 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-lg shadow-blue-500/20'
                        : 'border-gray-200 bg-white/50 hover:border-blue-300 hover:bg-blue-50/50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold text-gray-800 group-hover:text-blue-700 transition-colors">
                          🇬🇷 Greece
                        </h3>
                        <p className="text-sm text-gray-600 mt-1">
                          Greek national law and legislation
                        </p>
                      </div>
                      {tempLawType === 'greek' && (
                        <div className="w-5 h-5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center">
                          <div className="w-2 h-2 bg-white rounded-full"></div>
                        </div>
                      )}
                    </div>
                  </button>
                </div>
              </div>

              {/* CTA Button */}
              <button
                onClick={handleModalConfirm}
                className="relative w-full group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-4 px-6 rounded-2xl transition-all duration-300 shadow-lg hover:shadow-xl hover:shadow-blue-500/25 hover:scale-105"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur-lg opacity-75 group-hover:opacity-100 transition-opacity duration-300"></div>
                <span className="relative flex items-center justify-center gap-2">
                  <Sparkles className="w-5 h-5" />
                  Start Legal Consultation
                </span>
              </button>

              {/* Footer Note */}
              <p className="text-xs text-gray-500 text-center mt-6 bg-gray-50/50 rounded-full px-4 py-2">
                You can change jurisdiction later in the settings
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Animated Background Pattern */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-r from-blue-400/20 to-purple-600/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-r from-indigo-400/20 to-cyan-600/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Header */}
        <header className="backdrop-blur-xl bg-white/80 border-b border-white/20 px-6 py-4 shadow-lg shadow-blue-500/5">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur-lg opacity-75"></div>
                <div className="relative bg-gradient-to-r from-blue-600 to-indigo-600 p-3 rounded-2xl">
                  <Scale className="w-7 h-7 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                  LawChecker
                </h1>
                <p className="text-sm text-gray-600 font-medium">Your smart legal assistant</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {/* <div className="hidden md:flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-full border border-blue-100">
                <Sparkles className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-700">AI-Powered</span>
              </div> */}

              {/* Jurisdiction Dropdown - Only show after modal is closed */}
              {!showModal && lawType && (
                <div className="relative flex flex-col items-center text-center">
                  <label className="block text-xs font-medium text-gray-500 mb-1">Jurisdiction:</label>
                  <div className="relative w-full max-w-[200px]">
                    <select
                      value={lawType}
                      onChange={(e) => handleLawTypeChange(e.target.value)}
                      className="appearance-none bg-white/80 backdrop-blur-sm border border-white/40 text-gray-800 text-sm rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full pl-4 pr-10 py-2.5 shadow-lg transition-all duration-300 hover:bg-white/90 font-medium min-w-[140px]"
                    >
                      <option value="un">United Nations</option>
                      <option value="greek">Greece</option>
                    </select>
                    <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
                  </div>
                </div>
              )}

            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-6 py-8">
          {/* Welcome Section */}
          {chatHistory.length === 1 && !showModal && (
            <div className="text-center mb-12 animate-fade-in">
              <div className="mb-8">
                <h2 className="text-4xl font-bold text-gray-800 mb-4">
                  Welcome to <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">LawChecker</span>
                </h2>
                <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
                  Search legal answers with confidence. Your AI-powered legal assistant is here to guide you.
                </p>
                {lawType && (
                  <div className="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-full border border-blue-100">
                    <Scale className="w-4 h-4 text-blue-600" />
                    <span className="text-sm text-blue-700 font-medium">
                      Active: {getLawTypeDisplay()}
                    </span>
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto mb-8">
                {quickQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => setUserMessage(question)}
                    className="p-4 bg-white/70 backdrop-blur-sm hover:bg-white/90 border border-white/40 hover:border-blue-200 rounded-2xl text-left transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10 hover:scale-105 group"
                  >
                    <span className="text-gray-700 group-hover:text-blue-700 transition-colors font-medium">
                      {question}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 overflow-y-auto mb-6 space-y-6">
            {chatHistory.map((message, index) => (
              <div
                key={index}
                className={`flex gap-4 animate-fade-in ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                {message.role === 'lawchecker' && (
                  <div className="relative flex-shrink-0 mt-1">
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full blur-md opacity-75"></div>
                    <div className="relative bg-gradient-to-r from-blue-500 to-indigo-600 p-3 rounded-full">
                      <MessageCircle className="w-5 h-5 text-white" />
                    </div>
                  </div>
                )}

                <div
                  className={`max-w-2xl rounded-3xl px-6 py-4 backdrop-blur-sm transition-all duration-300 ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/25 rounded-br-lg'
                      : 'bg-white/80 text-gray-800 border border-white/40 shadow-lg shadow-gray-500/10 rounded-bl-lg hover:bg-white/90'
                  }`}
                >
                  <p className="text-sm leading-relaxed whitespace-pre-wrap font-medium">{message.text}</p>
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <button
                        onClick={() => {
                          const updated = [...chatHistory];
                          updated[index].showSources = !updated[index].showSources;
                          setChatHistory(updated);
                        }}
                        className="text-xs text-blue-600 hover:underline font-medium"
                      >
                        {message.showSources ? (isGreek(message.text) ? 'Απόκρυψη Πηγών' : 'Hide Sources') : (isGreek(message.text) ? 'Προβολή Πηγών' : 'Show Sources')}
                      </button>

                      {message.showSources && (
                        <>
                          <h4 className="text-xs font-semibold text-gray-500 uppercase">Sources</h4>
                          <ul className="space-y-2 text-sm text-gray-600">
                            {message.sources.map((src, idx) => (
                              <SourceItem
                                key={idx}
                                source={src.source}
                                snippet={src.snippet}
                                articles={src.articles}
                              />
                            ))}
                          </ul>
                        </>
                      )}
                    </div>
                  )}

                </div>

                {message.role === 'user' && (
                  <div className="bg-gradient-to-r from-gray-100 to-gray-200 p-3 rounded-full flex-shrink-0 mt-1 shadow-md">
                    <User className="w-5 h-5 text-gray-600" />
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="flex gap-4 justify-start animate-fade-in">
                <div className="relative flex-shrink-0 mt-1">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full blur-md opacity-75"></div>
                  <div className="relative bg-gradient-to-r from-blue-500 to-indigo-600 p-3 rounded-full">
                    <MessageCircle className="w-5 h-5 text-white" />
                  </div>
                </div>
                <div className="bg-white/80 backdrop-blur-sm border border-white/40 rounded-3xl rounded-bl-lg px-6 py-4 shadow-lg">
                  <div className="flex gap-2">
                    <div className="w-2.5 h-2.5 bg-blue-500 rounded-full animate-bounce"></div>
                    <div className="w-2.5 h-2.5 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2.5 h-2.5 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area - Only show after modal is closed */}
          {!showModal && (
            <div className="backdrop-blur-xl bg-white/80 border border-white/30 rounded-3xl shadow-2xl shadow-blue-500/10 p-6 transition-all duration-300 hover:shadow-blue-500/20">
              <div className="flex gap-4 items-end">
                <div className="flex-1">
                  <textarea
                    value={userMessage}
                    onChange={e => setUserMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Describe your legal question here..."
                    className="w-full resize-none border-0 outline-none text-gray-800 placeholder-gray-500 bg-transparent text-base leading-relaxed font-medium"
                    rows="3"
                    disabled={isLoading}
                  />
                </div>
                <button
                  onClick={handleSend}
                  disabled={!userMessage.trim() || isLoading}
                  className="relative group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-300 disabled:to-gray-400 text-white p-4 rounded-2xl transition-all duration-300 disabled:cursor-not-allowed shadow-lg hover:shadow-xl hover:shadow-blue-500/25 hover:scale-105 disabled:hover:scale-100"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur-lg opacity-75 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <Send className="relative w-5 h-5" />
                </button>
              </div>
            </div>
          )}

          {/* Footer */}
          {!showModal && (
            <div className="text-center mt-6">
              <p className="text-xs text-gray-500 bg-white/50 backdrop-blur-sm rounded-full px-4 py-2 inline-block border border-white/30">
                🛡️ Answers are provided for informational purposes only • Consult a legal professional for specific cases
              </p>
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.6s ease-out forwards;
        }
      `}</style>
    </div>
  );
}

export default App;

function SourceItem({ source, snippet, articles }) {
  const [expanded, setExpanded] = useState(false);
  const isGreek = source.match(/[Α-Ωα-ω]/);
  const label = isGreek ? 'Άρθρα' : 'Articles';

  const previewLength = 100;
  const showToggle = snippet.length > previewLength;
  const displayText = expanded ? snippet : snippet.slice(0, previewLength);

  return (
    <li className="bg-white/80 border border-blue-100 p-4 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300">
      <h5 className="text-sm font-semibold text-blue-800 mb-1">📄 {source}</h5>
      {articles && articles.length > 0 && (
        <p className="text-xs text-gray-500 mb-2">
          🧩 {label}: {articles.join(', ')}
        </p>
      )}
      <p className="text-gray-700 text-sm leading-snug whitespace-pre-wrap">
        {displayText}
        {showToggle && (
          <>
            {!expanded && '... '}
            <button
              onClick={() => setExpanded(prev => !prev)}
              className="ml-1 text-blue-600 hover:underline text-xs font-medium"
            >
              {expanded ? (isGreek ? 'Λιγότερα' : 'Show less') : (isGreek ? 'Περισσότερα' : 'Show more')}
            </button>
          </>
        )}
      </p>
    </li>
  );
}
