"""
Gateway per Google Calendar - Dependency injection pattern con booking reali
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import logging

logger = logging.getLogger(__name__)

class CalendarError(Exception):
    """Eccezione specifica per errori del calendario"""
    pass

class CalendarGateway(ABC):
    """Interfaccia astratta per il calendar gateway"""
    
    @abstractmethod
    async def get_available_slots(self, date: datetime = None, consultation_type: str = "presenza") -> List[datetime]:
        """Ottiene slot disponibili"""
        pass
    
    @abstractmethod
    async def book_appointment(self, client_phone: str, client_name: str, start_time: datetime, 
                             duration_minutes: int = 60, description: str = "") -> Dict[str, Any]:
        """Prenota appuntamento"""
        pass
    
    @abstractmethod
    async def is_slot_available(self, slot_datetime: datetime) -> bool:
        """Verifica se uno slot è disponibile"""
        pass
    
    @abstractmethod
    async def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancella appuntamento"""
        pass

class GoogleCalendarGateway(CalendarGateway):
    """Implementazione Google Calendar con booking reali"""
    
    def __init__(self, calendar_service=None, calendar_id: str = None):
        self.calendar_service = calendar_service
        self.calendar_id = calendar_id or "pierpaolo.laurito@gmail.com"
        self.working_hours = {
            "start": "09:00",
            "end": "18:00"
        }
        self.working_days = [0, 1, 2, 3, 4]  # Lun-Ven
    
    async def get_available_slots(self, date: datetime = None, consultation_type: str = "presenza") -> List[datetime]:
        """Ottiene slot disponibili reali da Google Calendar"""
        try:
            if not date:
                date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            
            # Se è passato l'orario di lavoro, passa al giorno successivo
            if date.hour >= 18:
                date = date + timedelta(days=1)
            
            # Trova il prossimo giorno lavorativo
            while date.weekday() not in self.working_days:
                date = date + timedelta(days=1)
            
            # Ottieni eventi esistenti per il giorno
            existing_events = await self._get_events_for_date(date)
            
            # Genera slot disponibili
            available_slots = []
            start_hour = 9
            end_hour = 18
            
            for hour in range(start_hour, end_hour):
                for minute in [0, 30]:  # Slot ogni 30 minuti
                    slot_time = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
                    # Verifica se lo slot è disponibile
                    if await self._is_slot_free(slot_time, existing_events):
                        available_slots.append(slot_time)
            
            # Ritorna massimo 6 slot
            return available_slots[:6]
            
        except Exception as e:
            logger.exception("Errore nel recupero slot disponibili")
            raise CalendarError(f"Impossibile recuperare slot disponibili: {e}")
    
    async def book_appointment(self, client_phone: str, client_name: str, start_time: datetime, 
                             duration_minutes: int = 60, description: str = "") -> Dict[str, Any]:
        """Prenota appuntamento reale su Google Calendar"""
        try:
            # Verifica disponibilità
            if not await self.is_slot_available(start_time):
                raise CalendarError(f"Slot {start_time} non più disponibile")
            
            # Crea evento su Google Calendar
            event = {
                'summary': f'Consulenza immigrazione - {client_name}',
                'description': f'''
Cliente: {client_name}
Telefono: {client_phone}
Descrizione: {description}
Studio: Via Monte Cengio 5, Milano
                '''.strip(),
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Europe/Rome',
                },
                'end': {
                    'dateTime': (start_time + timedelta(minutes=duration_minutes)).isoformat(),
                    'timeZone': 'Europe/Rome',
                },
                'location': 'Via Monte Cengio 5, 20145 Milano MI, Italia',
                'attendees': [
                    {'email': 'pierpaolo.laurito@gmail.com'},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            if self.calendar_service:
                # Booking reale
                created_event = self.calendar_service.events().insert(
                    calendarId=self.calendar_id,
                    body=event
                ).execute()
                
                logger.info(f"✅ Appuntamento creato su Google Calendar: {created_event['id']}")
                
                return {
                    "success": True,
                    "appointment_id": created_event['id'],
                    "datetime": start_time,
                    "formatted_datetime": start_time.strftime("%d/%m %H:%M"),
                    "client_name": client_name,
                    "calendar_url": created_event.get('htmlLink'),
                    "message": f"Appuntamento confermato per {start_time.strftime('%d/%m alle %H:%M')}"
                }
            else:
                # Fallback mock
                logger.warning("⚠️ Calendar service non disponibile, usando mock")
                return {
                    "success": True,
                    "appointment_id": f"mock_{int(asyncio.get_event_loop().time())}",
                    "datetime": start_time,
                    "formatted_datetime": start_time.strftime("%d/%m %H:%M"),
                    "client_name": client_name,
                    "message": f"Appuntamento confermato per {start_time.strftime('%d/%m alle %H:%M')} (MOCK)"
                }
                
        except Exception as e:
            logger.exception("Errore nel booking appuntamento")
            raise CalendarError(f"Impossibile prenotare appuntamento: {e}")
    
    async def is_slot_available(self, slot_datetime: datetime) -> bool:
        """Verifica se uno slot è disponibile"""
        try:
            existing_events = await self._get_events_for_date(slot_datetime)
            return await self._is_slot_free(slot_datetime, existing_events)
        except Exception as e:
            logger.error(f"Errore nel controllo disponibilità slot: {e}")
            return False
    
    async def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancella appuntamento"""
        try:
            if self.calendar_service:
                self.calendar_service.events().delete(
                    calendarId=self.calendar_id,
                    eventId=appointment_id
                ).execute()
                logger.info(f"✅ Appuntamento cancellato: {appointment_id}")
                return True
            else:
                logger.warning(f"⚠️ Calendar service non disponibile, mock cancellation: {appointment_id}")
                return True
        except Exception as e:
            logger.error(f"Errore nella cancellazione appuntamento: {e}")
            return False
    
    async def _get_events_for_date(self, date: datetime) -> List[Dict]:
        """Ottiene eventi per una data specifica"""
        try:
            if not self.calendar_service:
                return []
            
            start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_time = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            events_result = self.calendar_service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_time.isoformat() + 'Z',
                timeMax=end_time.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
            
        except Exception as e:
            logger.error(f"Errore nel recupero eventi: {e}")
            return []
    
    async def _is_slot_free(self, slot_time: datetime, existing_events: List[Dict]) -> bool:
        """Verifica se uno slot è libero"""
        slot_end = slot_time + timedelta(hours=1)
        
        for event in existing_events:
            event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
            
            # Verifica sovrapposizione
            if (slot_time < event_end and slot_end > event_start):
                return False
        
        return True

# FakeCalendarGateway rimosso - solo implementazione Google Calendar in produzione 