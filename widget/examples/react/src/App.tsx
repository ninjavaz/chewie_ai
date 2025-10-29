import { ChewieChat, type ChewieEvent } from '@chewieai/chat-widget';
import '@chewieai/chat-widget/styles.css';
import chewieaiLogo from './chewieai-logo.png';


function App() {
  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1 className="title">
            <span className="logo">🚀</span>
            DeFi Protocol Dashboard
          </h1>
          <p className="subtitle">Kamino Finance Demo</p>
        </div>
      </header>

      <main className="main">
        <div className="container">
          <div className="hero">
            <h2>Welcome to Your DeFi Dashboard</h2>
            <p>
              Track your yields, manage liquidity, and get AI-powered insights with Chewie.
            </p>
            <div className="stats">
              <div className="stat-card">
                <div className="stat-value">$124.5K</div>
                <div className="stat-label">Total Value Locked</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">12.4%</div>
                <div className="stat-label">Avg APR</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">$1,245</div>
                <div className="stat-label">Monthly Earnings</div>
              </div>
            </div>
          </div>

          <div className="info-section">
            <h3>Try Chewie AI</h3>
            <p>Click the chat button in the bottom-right corner to:</p>
            <ul>
              <li>Ask about Kamino pools and APRs</li>
              <li>Calculate earnings estimates</li>
              <li>Get DeFi explanations and support</li>
            </ul>
            <div className="demo-queries">
              <strong>Example queries:</strong>
              <code>"How much can I earn on 1000 USDC in Allez pool?"</code>
              <code>"What is Kamino Finance?"</code>
              <code>"How does lending work?"</code>
            </div>
          </div>
        </div>
      </main>

      <ChewieChat
        apiUrl={import.meta.env.VITE_CHEWIE_API_URL || 'http://localhost:8000'}
        dapp="kamino"
        lang="en"
        theme="dark"
        position="bottom-right"
        avatarUrl={chewieaiLogo}
        mock={true}
        initialPrompts={[
          'How much can I earn on 1000 USDC?',
          'What is Kamino?',
          'How does lending work?',
        ]}
        onEvent={(event: ChewieEvent) => {
          console.log('Chewie event:', event);
        }}
      />
    </div>
  );
}

export default App;
