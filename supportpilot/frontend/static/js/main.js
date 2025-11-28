const API_BASE = (location.hostname === 'localhost' || location.hostname === '127.0.0.1') ? 'http://localhost:5000' : ''

async function createTicket(e){
  e && e.preventDefault()
  const user_id = document.getElementById('user_id').value
  const subject = document.getElementById('subject').value
  const message = document.getElementById('message').value
  const payload = {user_id, subject, message}
  const res = await fetch(API_BASE + '/create_ticket', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)})
  const j = await res.json()
  loadTickets(user_id)
}

async function loadTickets(user_id){
  const qs = user_id ? '?user_id=' + encodeURIComponent(user_id) : ''
  const res = await fetch(API_BASE + '/get_tickets' + qs)
  const j = await res.json()
  const list = document.getElementById('tickets')
  if(!list) return
  list.innerHTML = ''
  const tickets = j.tickets || []
  for(const t of tickets){
    const li = document.createElement('li')
    li.innerHTML = `<strong>${t.subject || t.id}</strong> - ${t.category || ''} - ${t.status || ''} <a href="/ticket.html?id=${t.id}">view</a>`
    list.appendChild(li)
  }
}

async function loadTicketDetail(){
  const params = new URLSearchParams(location.search)
  const id = params.get('id')
  if(!id) return
  const res = await fetch(API_BASE + '/get_tickets')
  const j = await res.json()
  const tickets = j.tickets || []
  const t = tickets.find(x=>x.id===id)
  if(!t) return
  document.getElementById('subject').innerText = t.subject || t.id
  document.getElementById('meta').innerText = 'Category: ' + (t.category||'') + ' | Status: ' + (t.status||'')
  const msgs = await fetch(API_BASE + `/get_tickets?user_id=${encodeURIComponent(t.user_id)}`)
  const mj = await msgs.json()
  const messages = t.messages || []
  const ul = document.getElementById('messages')
  ul.innerHTML = ''
  for(const m of messages){
    const li = document.createElement('li')
    li.innerText = `${m.sender}: ${m.message}`
    ul.appendChild(li)
  }
}

async function sendReply(e){
  e && e.preventDefault()
  const params = new URLSearchParams(location.search)
  const id = params.get('id')
  const responder = document.getElementById('responder').value
  const reply = document.getElementById('reply').value
  if(!id) return
  await fetch(API_BASE + '/assign_agent', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ticket_id:id, agent_id:responder})})
  await fetch(API_BASE + '/auto_reply', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({text:reply, role:'agent'})})
  location.reload()
}

async function faqSearch(){
  const term = document.getElementById('faq-search').value
  const res = await fetch(API_BASE + '/get_faq?q=' + encodeURIComponent(term))
  const j = await res.json()
  const list = document.getElementById('faq-list')
  list.innerHTML = ''
  for(const e of j.faq || []){
    const li = document.createElement('li')
    li.innerHTML = `<strong>${e.question}</strong><div>${e.answer}</div>`
    list.appendChild(li)
  }
}

document.addEventListener('DOMContentLoaded', ()=>{
  if(document.getElementById('ticket-form')){
    document.getElementById('ticket-form').addEventListener('submit', createTicket)
    const uid = document.getElementById('user_id').value || ''
    if(uid) loadTickets(uid)
  }
  if(document.getElementById('tickets')){
    const uid = ''
    loadTickets(uid)
  }
  if(document.getElementById('reply-form')){
    document.getElementById('reply-form').addEventListener('submit', sendReply)
    loadTicketDetail()
  }
  if(document.getElementById('faq-go')){
    document.getElementById('faq-go').addEventListener('click', faqSearch)
  }
})
