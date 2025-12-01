import React, { useEffect, useState } from 'react'
import api from '../api/client'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

const COLORS = ['#16a34a', '#f59e0b', '#ef4444']

export default function AdminDashboard(){
  const [stats, setStats] = useState(null)

  useEffect(()=>{
    async function load(){
      try{
        const res = await api.get('/analytics/dashboard')
        setStats(res.data.data || {})
      }catch(e){
        console.warn(e)
        setStats({}) // Set empty stats on error
      }
    }
    load()
  }, [])

  const sentiment = stats?.sentiment || {positive:0, neutral:0, negative:0}
  const tickets = stats?.tickets || {total_tickets:0, open_tickets:0, in_progress_tickets:0, resolved_tickets:0}
  const hasSentimentData = sentiment.positive + sentiment.neutral + sentiment.negative > 0

  return (
    <div className="page">
      <h2 className="page-title">Admin Dashboard</h2>
      {stats === null && <div className="loading">Loading analytics...</div>}
      {stats !== null && (
        <div className="charts">
          <div className="chart-card">
            <h4>📈 Ticket Statistics</h4>
            <div className="stats-grid">
              <div className="stat-item"><span className="stat-label">Total:</span> <span className="stat-value">{tickets.total_tickets}</span></div>
              <div className="stat-item"><span className="stat-label">Open:</span> <span className="stat-value open">{tickets.open_tickets}</span></div>
              <div className="stat-item"><span className="stat-label">In Progress:</span> <span className="stat-value progress">{tickets.in_progress_tickets}</span></div>
              <div className="stat-item"><span className="stat-label">Resolved:</span> <span className="stat-value resolved">{tickets.resolved_tickets}</span></div>
            </div>
          </div>

          <div className="chart-card">
            <h4>😊 Sentiment Distribution</h4>
            {hasSentimentData ? (
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie dataKey="value" data={[{name:'positive', value: sentiment.positive},{name:'neutral', value: sentiment.neutral},{name:'negative', value: sentiment.negative}]}>
                    {[{name:'positive'},{name:'neutral'},{name:'negative'}].map((entry, idx) => (
                      <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="no-data">No sentiment data yet. Create tickets to see analytics!</div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
