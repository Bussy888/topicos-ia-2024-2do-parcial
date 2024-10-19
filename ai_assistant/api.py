from fastapi import FastAPI, Depends, Query
from llama_index.core.agent import ReActAgent
from ai_assistant.agent import TravelAgent
from ai_assistant.models import AgentAPIResponse
from ai_assistant.tools import (
    reserve_bus,
    reserve_flight,
    reserve_hotel,
    reserve_restaurant,
    generate_trip_summary
)


def get_agent() -> ReActAgent:
    return TravelAgent().get_agent()


app = FastAPI(title="AI Agent")


@app.get("/recommendations/cities")
def recommend_cities(
    notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"recommend cities in bolivia with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
@app.get("/recommendations/places")
def recommend_places(city: str, notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)):
    
    prompt = f"recommend places to visit in {city} with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))

@app.get("/recommendations/hotels")
def recommend_hotels(city: str, notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)):
    prompt = f"recommend hotels in {city} with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))

@app.get("/recommendations/activities")
def recommend_activities(city: str, notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)):
    prompt = f"recommend activities in {city} with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))

@app.post("/reserve/bus")
def reserve_bus_ticket(origin: str, destination: str, date: str):
    reservation = reserve_bus(date, origin, destination)
    return {"status": "OK", "reservation": reservation.dict()}

@app.post("/reserve/flight")
def reserve_flight_ticket(origin: str, destination: str, date: str):
    reservation = reserve_flight(date, origin, destination)
    return {"status": "OK", "reservation": reservation.dict()}
@app.post("/reserve/hotel")
def reserve_hotel_room(checkin_date: str, checkout_date: str, hotel: str, city: str):
    reservation = reserve_hotel(checkin_date, checkout_date, hotel, city)
    return {"status": "OK", "reservation": reservation.dict()}
@app.post("/reserve/restaurant")
def reserve_restaurant_table(date: str, hour: str, restaurant: str, city: str, dish: str = None):
    reservation_time = f"{date}T{hour}"
    reservation = reserve_restaurant(reservation_time, restaurant, city, dish)
    return {"status": "OK", "reservation": reservation.dict()}


@app.get("/trip/report")
def trip_report(agent: ReActAgent = Depends(get_agent)):
    report = generate_trip_summary()
    return AgentAPIResponse(status="OK", agent_response=report)