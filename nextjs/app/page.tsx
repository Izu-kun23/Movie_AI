'use client';

import { useState, useRef, useEffect } from 'react';
import './page.css';

interface Movie {
  title: string;
  overview: string;
  similarity_score?: number;
  explanation?: string;
  poster?: string;
}

interface ChatResponse {
  type: 'greeting' | 'recommendations' | 'search_results' | 'error';
  message: string;
  requested_movie?: string;
  recommendations?: Movie[];
  movies?: Movie[];
}

export default function Home() {
  const [messages, setMessages] = useState<Array<{
    text: string;
    sender: 'user' | 'ai';
    type?: string;
    recommendations?: Movie[];
    movies?: Movie[];
    requestedMovie?: string;
  }>>([
    {
      text: "Hello! I'm your AI movie recommendation assistant. Tell me a movie you like, and I'll find similar ones for you! 🎬",
      sender: 'ai'
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Use Next.js API route (proxies to backend)
  const API_BASE_URL = '/api';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const detectIntent = (message: string): string => {
    const lowerMsg = message.toLowerCase();
    if (lowerMsg.match(/hello|hi|hey|greetings/i)) {
      return 'greeting';
    } else if (lowerMsg.match(/search|find|look for/i)) {
      return 'search';
    }
    return 'recommend';
  };

  const handleSendMessage = async () => {
    const message = input.trim();
    if (!message) return;

    setInput('');
    setMessages(prev => [...prev, { text: message, sender: 'user' }]);
    setIsTyping(true);

    try {
      const msgType = detectIntent(message);
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, type: msgType })
      });

      if (!response.ok) {
        throw new Error('Request failed');
      }

      const data: ChatResponse = await response.json();
      setIsTyping(false);

      if (data.type === 'greeting') {
        setMessages(prev => [...prev, { text: data.message, sender: 'ai' }]);
      } else if (data.type === 'recommendations') {
        setMessages(prev => [...prev, {
          text: data.message,
          sender: 'ai',
          type: 'recommendations',
          recommendations: data.recommendations,
          requestedMovie: data.requested_movie
        }]);
      } else if (data.type === 'search_results') {
        setMessages(prev => [...prev, {
          text: data.message,
          sender: 'ai',
          type: 'search',
          movies: data.movies
        }]);
      } else {
        setMessages(prev => [...prev, { text: data.message, sender: 'ai' }]);
      }
    } catch (error: any) {
      setIsTyping(false);
      setMessages(prev => [...prev, {
        text: `Sorry, I encountered an error: ${error.message}`,
        sender: 'ai'
      }]);
    }
  };

  const handleSuggestion = (message: string) => {
    setInput(message);
    setTimeout(() => handleSendMessage(), 100);
  };

  const chatRecommendFor = (movieTitle: string) => {
    setInput(`I like ${movieTitle}`);
    setTimeout(() => handleSendMessage(), 100);
  };

  return (
    <div className="container">
      <header className="header">
        <div className="header__content">
          <h1 className="header__title">
            <span className="header__icon">🤖</span>
            Movie AI Assistant
          </h1>
          <p className="header__subtitle">Your intelligent movie recommendation companion</p>
        </div>
      </header>

      <main className="main">
        <div className="chat-container">
          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <Message
                key={idx}
                text={msg.text}
                sender={msg.sender}
                recommendations={msg.recommendations}
                movies={msg.movies}
                onRecommendClick={chatRecommendFor}
              />
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <div className="chat-input-wrapper">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                className="chat-input"
                placeholder="Try: 'I like The Matrix' or 'Recommend movies similar to Inception'"
              />
              <button onClick={handleSendMessage} className="chat-send-btn">
                <span className="chat-send-icon">✨</span>
              </button>
            </div>
            <div className="chat-suggestions">
              <button
                className="suggestion-btn"
                onClick={() => handleSuggestion('I like The Matrix')}
              >
                🎬 The Matrix
              </button>
              <button
                className="suggestion-btn"
                onClick={() => handleSuggestion('Recommend something like Inception')}
              >
                🌌 Inception
              </button>
              <button
                className="suggestion-btn"
                onClick={() => handleSuggestion('Find movies similar to Blade Runner')}
              >
                🔮 Blade Runner
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>Powered by AI • FastAPI & Scikit-learn</p>
      </footer>
    </div>
  );
}

function Message({ text, sender, recommendations, movies, onRecommendClick }: {
  text: string;
  sender: 'user' | 'ai';
  recommendations?: Movie[];
  movies?: Movie[];
  onRecommendClick: (title: string) => void;
}) {
  return (
    <div className={`message message--${sender}`}>
      {sender === 'ai' && <div className="message__avatar">🤖</div>}
      <div className="message__content">
        <p>{text}</p>
        {recommendations && (
          <div className="recommendations-container">
            {recommendations.map((movie, idx) => (
              <MovieCard key={idx} movie={movie} onRecommendClick={onRecommendClick} />
            ))}
          </div>
        )}
        {movies && (
          <div className="search-results-container">
            {movies.map((movie, idx) => (
              <SearchResultItem key={idx} movie={movie} onRecommendClick={onRecommendClick} />
            ))}
          </div>
        )}
        <span className="message__time">{new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
      </div>
      {sender === 'user' && <div className="message__avatar">👤</div>}
    </div>
  );
}

function MovieCard({ movie, onRecommendClick }: { movie: Movie; onRecommendClick: (title: string) => void }) {
  const similarityPercent = movie.similarity_score ? (movie.similarity_score * 100).toFixed(1) : '0';

  return (
    <div className="movie-card-chat">
      {movie.poster && (
        <div className="movie-card-chat__poster">
          <img src={movie.poster} alt={movie.title} onError={(e) => {
            (e.target as HTMLImageElement).style.display = 'none';
          }} />
        </div>
      )}
      <div className="movie-card-chat__content">
        <div className="movie-card-chat__header">
          <h3 className="movie-card-chat__title">{movie.title}</h3>
          <span className="movie-card-chat__match">{similarityPercent}% match</span>
        </div>
        <p className="movie-card-chat__overview">{movie.overview}</p>
        {movie.explanation && (
          <div className="movie-card-chat__explanation">
            💡 {movie.explanation}
          </div>
        )}
        <button
          className="movie-card-chat__btn"
          onClick={() => onRecommendClick(movie.title)}
        >
          Get similar movies
        </button>
      </div>
    </div>
  );
}

function SearchResultItem({ movie, onRecommendClick }: { movie: Movie; onRecommendClick: (title: string) => void }) {
  return (
    <div className="search-result-item">
      {movie.poster && (
        <div className="search-result-item__poster">
          <img src={movie.poster} alt={movie.title} onError={(e) => {
            (e.target as HTMLImageElement).style.display = 'none';
          }} />
        </div>
      )}
      <div className="search-result-item__content">
        <h4 className="search-result-item__title">{movie.title}</h4>
        <p className="search-result-item__overview">{movie.overview}</p>
        <button
          className="search-result-item__btn"
          onClick={() => onRecommendClick(movie.title)}
        >
          Get recommendations
        </button>
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="typing-indicator">
      <div className="message message--ai">
        <div className="message__avatar">🤖</div>
        <div className="message__content">
          <div className="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
  );
}
