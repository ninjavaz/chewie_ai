import React, { useState } from 'react';
import { ChewieWidget } from '../ChewieWidget';
import type { ChewieWidgetProps } from '../types';

const App: React.FC = () => {
  const [config, setConfig] = useState<ChewieWidgetProps>({
    endpoint: 'https://chewie.ai/api/ask',
    protocol: 'aave',
    theme: 'auto',
    position: 'bottom-right',
    language: 'en',
    enableFeedback: true,
    welcomeMessage: "Hi! I'm ChewieAI, your DeFi assistant. How can I help you today?",
    placeholder: "Ask me anything about DeFi...",
  });

  const handleConfigChange = (key: keyof ChewieWidgetProps, value: any) => {
    setConfig(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      padding: '40px 20px',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white'
    }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <header style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '16px', fontWeight: '700' }}>
            🤖 ChewieAI Widget
          </h1>
          <p style={{ fontSize: '1.2rem', opacity: 0.9 }}>
            AI-powered chat widget for DeFi protocols and dApps
          </p>
        </header>

        <div style={{ 
          background: 'rgba(255, 255, 255, 0.1)', 
          borderRadius: '16px', 
          padding: '32px',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <h2 style={{ marginBottom: '24px', fontSize: '1.5rem' }}>Configuration</h2>
          
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
            gap: '20px',
            marginBottom: '32px'
          }}>
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
                Theme
              </label>
              <select
                value={config.theme}
                onChange={(e) => handleConfigChange('theme', e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  border: 'none',
                  background: 'rgba(255, 255, 255, 0.9)',
                  color: '#333'
                }}
              >
                <option value="auto">Auto</option>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
                Position
              </label>
              <select
                value={config.position}
                onChange={(e) => handleConfigChange('position', e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  border: 'none',
                  background: 'rgba(255, 255, 255, 0.9)',
                  color: '#333'
                }}
              >
                <option value="bottom-right">Bottom Right</option>
                <option value="bottom-left">Bottom Left</option>
                <option value="top-right">Top Right</option>
                <option value="top-left">Top Left</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
                Protocol
              </label>
              <input
                type="text"
                value={config.protocol || ''}
                onChange={(e) => handleConfigChange('protocol', e.target.value)}
                placeholder="e.g., aave, compound, uniswap"
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  border: 'none',
                  background: 'rgba(255, 255, 255, 0.9)',
                  color: '#333'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
                Language
              </label>
              <select
                value={config.language}
                onChange={(e) => handleConfigChange('language', e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  border: 'none',
                  background: 'rgba(255, 255, 255, 0.9)',
                  color: '#333'
                }}
              >
                <option value="en">English</option>
                <option value="pl">Polish</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="zh">Chinese</option>
              </select>
            </div>
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={config.enableFeedback}
                onChange={(e) => handleConfigChange('enableFeedback', e.target.checked)}
                style={{ transform: 'scale(1.2)' }}
              />
              Enable Feedback Buttons
            </label>
          </div>

          <div style={{ 
            background: 'rgba(0, 0, 0, 0.2)', 
            borderRadius: '12px', 
            padding: '20px',
            fontFamily: 'Monaco, Consolas, "Courier New", monospace',
            fontSize: '14px',
            overflow: 'auto'
          }}>
            <h3 style={{ marginBottom: '16px', color: '#fff' }}>Usage Example:</h3>
            <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
{`import { ChewieWidget } from '@chewieai/widget';

<ChewieWidget
  endpoint="${config.endpoint}"
  protocol="${config.protocol || 'aave'}"
  theme="${config.theme}"
  position="${config.position}"
  language="${config.language}"
  enableFeedback={${config.enableFeedback}}
  welcomeMessage="${config.welcomeMessage}"
  placeholder="${config.placeholder}"
/>`}
            </pre>
          </div>
        </div>

        <div style={{ 
          marginTop: '40px', 
          textAlign: 'center',
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '16px',
          padding: '24px',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <h3 style={{ marginBottom: '16px' }}>Installation</h3>
          <code style={{ 
            background: 'rgba(0, 0, 0, 0.3)', 
            padding: '8px 16px', 
            borderRadius: '8px',
            fontSize: '16px'
          }}>
            npm install @chewieai/widget
          </code>
        </div>
      </div>

      <ChewieWidget {...config} />
    </div>
  );
};

export default App;
