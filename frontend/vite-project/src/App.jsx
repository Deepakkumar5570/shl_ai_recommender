import { useState, useEffect, useRef } from "react";

export default function App() {

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I can help you discover SHL assessments for hiring and workforce evaluation.",
    },
  ]);

  const [recommendations, setRecommendations] = useState([]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const handleSend = async () => {

    if (!input.trim() || loading) return;

    const updatedMessages = [
      ...messages,
      {
        role: "user",
        content: input,
      },
    ];

    setMessages(updatedMessages);

    setInput("");

    setLoading(true);

    try {

      //latest deploy

      const response = await fetch(
        "https://shl-ai-recommender-ue80.onrender.com/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            messages: updatedMessages,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Backend Error");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply || "No response received.",
        },
      ]);

      setRecommendations(
        Array.isArray(data.recommendations)
          ? data.recommendations
          : []
      );

    } catch (error) {

      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Backend connection failed.",
        },
      ]);

    }

    setLoading(false);
  };

  return (

    <div className="min-h-screen bg-gradient-to-br from-white via-slate-50 to-blue-50">

      {/* NAVBAR */}

      <div className="border-b border-slate-200 bg-white">

        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">

          <div>

            <h1 className="text-3xl font-bold text-slate-900">
              SHL AI Recommender
            </h1>

            <p className="text-slate-500 mt-1">
              Conversational SHL assessment recommendation platform
            </p>

          </div>

          <div className="flex items-center gap-3">

            <div className="h-3 w-3 rounded-full bg-green-500"></div>

            <span className="text-slate-600 font-medium">
              AI Online
            </span>

          </div>

        </div>

      </div>

      {/* MAIN */}

      <div className="max-w-7xl mx-auto px-6 py-8">

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">

          {/* CHAT SECTION */}

          <div className="xl:col-span-2">

            <div className="bg-white border border-slate-200 rounded-[32px] shadow-sm h-[820px] flex flex-col overflow-hidden">

              {/* HEADER */}

              <div className="px-8 py-6 border-b border-slate-100">

                <h2 className="text-2xl font-bold text-slate-900">
                  AI Hiring Assistant
                </h2>

                <p className="text-slate-500 mt-2">
                  Ask hiring and workforce evaluation related queries.
                </p>

              </div>

              {/* MESSAGES */}

              <div className="flex-1 overflow-y-auto px-8 py-8 space-y-6 bg-slate-50/40">

                {messages.map((message, index) => (

                  <div
                    key={index}
                    className={`flex ${message.role === "user"
                        ? "justify-end"
                        : "justify-start"
                      }`}
                  >

                    <div
                      className={`max-w-2xl rounded-3xl px-6 py-5 shadow-sm ${message.role === "user"
                          ? "bg-blue-600 text-white rounded-br-md"
                          : "bg-white border border-slate-200 text-slate-800 rounded-bl-md"
                        }`}
                    >

                      <p className="leading-relaxed whitespace-pre-line">
                        {message.content}
                      </p>

                    </div>

                  </div>

                ))}

                {loading && (

                  <div className="flex justify-start">

                    <div className="bg-white border border-slate-200 rounded-3xl px-6 py-5 shadow-sm">

                      <p className="text-slate-500 animate-pulse">
                        Thinking...
                      </p>

                    </div>

                  </div>

                )}
                <div ref={messagesEndRef}></div>

              </div>

              {/* INPUT */}

              <div className="border-t border-slate-100 bg-white px-8 py-6">

                <div className="flex items-center gap-4">

                  <input
                    type="text"
                    placeholder="Describe your hiring requirement..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        handleSend();
                      }
                    }}
                    className="flex-1 border border-slate-300 rounded-2xl px-6 py-5 outline-none focus:ring-2 focus:ring-blue-500"
                  />

                  <button
                    onClick={handleSend}
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed text-white px-8 py-5 rounded-2xl font-semibold transition-all"
                  >
                    {loading ? "..." : "Send"}
                  </button>

                </div>

              </div>

            </div>

          </div>

          {/* RECOMMENDATIONS */}

          <div>

            <div className="bg-white border border-slate-200 rounded-[32px] shadow-sm h-[820px] overflow-hidden flex flex-col">

              <div className="px-7 py-6 border-b border-slate-100">

                <h2 className="text-2xl font-bold text-slate-900">
                  Recommended Assessments
                </h2>

              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-5 bg-slate-50/30">

                {recommendations.length === 0 ? (

                  <div className="text-slate-500 text-sm">
                    No recommendations yet.
                  </div>

                ) : (

                  recommendations.map((item, index) => (

                    <div
                      key={index}
                      className="bg-white border border-slate-200 rounded-3xl p-6 hover:shadow-lg transition-all"
                    >

                      <div className="flex items-start justify-between">

                        <div className="flex-1">

                          {/* TITLE */}

                          <h3 className="text-xl font-bold text-slate-900">

                            {item.name || "Unknown Assessment"}

                          </h3>

                          {/* TYPE */}

                          <div className="mt-3 inline-flex items-center bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-semibold">

                            {item.test_type || "Assessment"}

                          </div>

                        </div>

                        <div className="text-slate-400 font-bold">
                          #{index + 1}
                        </div>

                      </div>

                      {/* DESCRIPTION */}

                      <p className="mt-4 text-slate-600 text-sm leading-relaxed">

                        {item.description ||
                          "SHL assessment recommendation."}

                      </p>

                      {/* JOB LEVELS */}

                      {item.job_levels &&
                        item.job_levels.length > 0 && (

                          <div className="mt-4 flex flex-wrap gap-2">

                            {item.job_levels.slice(0, 3).map((level, idx) => (

                              <span
                                key={idx}
                                className="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-xs"
                              >
                                {level}
                              </span>

                            ))}

                          </div>

                        )}

                      {/* BUTTON */}

                      {item.url ? (

                        <a
                          href={item.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex mt-6 bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-2xl font-semibold transition-all"
                        >
                          View Assessment →
                        </a>

                      ) : (

                        <button
                          disabled
                          className="inline-flex mt-6 bg-gray-400 text-white px-5 py-3 rounded-2xl font-semibold cursor-not-allowed"
                        >
                          No URL Available
                        </button>

                      )}

                    </div>

                  ))

                )}

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}