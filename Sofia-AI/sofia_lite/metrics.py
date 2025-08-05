from prometheus_client import Counter

new_leads          = Counter("sofia_new_leads_total",
                             "Nuovi clienti indirizzati alla consulenza")
active_redirects   = Counter("sofia_active_app_redirect_total",
                             "Utenti attivi instradati all'app")
bookings_confirmed = Counter("sofia_bookings_confirmed_total",
                             "Appuntamenti fissati")
clarifies          = Counter("sofia_clarify_messages_total",
                             "Messaggi di chiarimento inviati") 