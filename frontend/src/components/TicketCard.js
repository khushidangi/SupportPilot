import React, { useState } from 'react'
import api from '../api/client'

export default function TicketCard({ ticket }){
  const role = typeof window !== 'undefined' ? localStorage.getItem('sp_role') : null
  const [status, setStatus] = useState(ticket.status || 'open')

  async function updateStatus(newStatus){
    try{
      setStatus(newStatus)
      await api.put(`/tickets/${ticket.ticket_id || ticket.id}/status`, { status: newStatus })
    }catch(e){
      console.warn('Failed to update status', e)
      setStatus(ticket.status || 'open')
    }
  }
  return (
    <div className="ticket-card">
      <div className="ticket-header">
        <strong className="ticket-title">{ticket.title || ticket.name}</strong>
        <div className="ticket-badges">
          <span className={`badge status-${ticket.status}`}>{ticket.status || 'open'}</span>
          {ticket.predicted_priority && (
            <span className={`badge priority-${ticket.predicted_priority}`}>{ticket.predicted_priority}</span>
          )}
        </div>
      </div>
      <div className="ticket-body">{ticket.description}</div>
      <div className="ticket-footer">
        <div className="ticket-meta">
          {ticket.sentiment_label && (
            <span className={`sentiment-icon sentiment-${ticket.sentiment_label}`} title={`Sentiment: ${ticket.sentiment_label}`}>
              {ticket.sentiment_label === 'positive' ? '😊' : ticket.sentiment_label === 'negative' ? '😞' : '😐'}
            </span>
          )}
          {ticket.keywords && ticket.keywords.length > 0 && (
            <span className="keywords" title={ticket.keywords.join(', ')}>
              🏷️ {ticket.keywords.slice(0,2).join(', ')}
            </span>
          )}
        </div>
        {role === 'agent' && (
          <span style={{marginLeft:12}}>
            <select value={status} onChange={e=>updateStatus(e.target.value)}>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="pending">Pending</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </span>
        )}
      </div>
    </div>
  )
}
