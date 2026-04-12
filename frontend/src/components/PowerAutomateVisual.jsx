import React, { useState } from 'react';
import './PowerAutomateVisual.css';

const PowerAutomateVisual = ({ visualId }) => {
  const [flowCreated, setFlowCreated] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');
  const [lastExecuted, setLastExecuted] = useState(null);

  const handleCreateFlow = (e) => {
    e.stopPropagation();
    console.log('Create Flow clicked');
    setFlowCreated(true);
  };

  const handleRunFlow = async (e) => {
    if (e) e.stopPropagation();
    console.log('Run Flow clicked');
    setIsRunning(true);
    setIsSuccess(false);
    setStatusMsg('Running automation...');
    
    try {
      const response = await fetch('/api/power-automate/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      console.log('API Response:', data);
      
      if (data.success) {
        setIsSuccess(true);
        setLastExecuted(data.executed_at);
        setStatusMsg('Success! Action triggered.');
        setTimeout(() => {
          setIsSuccess(false);
          setStatusMsg('');
        }, 3000);
      } else {
        alert('Flow execution failed: ' + (data.message || 'Unknown error'));
        setStatusMsg('Execution failed');
      }
    } catch (error) {
      console.error('Error running flow:', error);
      setStatusMsg('Network error. Check console.');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="pa-visual-container">
      <div className="pa-visual-header">
        <span className="pa-visual-zap">⚡</span>
        <span className="pa-visual-title">Power Automate</span>
      </div>
      
      <p className="pa-visual-subtitle">{statusMsg || 'Trigger an automation'}</p>
      
      {lastExecuted && (
        <div className="pa-visual-log">
          Last run: {lastExecuted}
        </div>
      )}

      {!flowCreated ? (
        <button className="pa-btn-create" onClick={handleCreateFlow} onMouseDown={(e) => e.stopPropagation()}>
          Create Flow
        </button>
      ) : (
        <button 
          className={`pa-btn-run ${isSuccess ? 'success' : ''}`} 
          onClick={handleRunFlow} 
          onMouseDown={(e) => e.stopPropagation()} 
          disabled={isRunning || isSuccess}
        >
          {isRunning ? 'Running...' : (isSuccess ? 'Success!' : 'Run Flow')}
        </button>
      )}
    </div>
  );
};

export default PowerAutomateVisual;
