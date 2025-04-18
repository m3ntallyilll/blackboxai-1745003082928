import os
import json
import time
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set GROQ_API_KEY environment variable directly for testing
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"  # Using Llama 3.3 70B for best tool use support

# Bot data for simulating responses
conversion_rates = {
    "beans": {
        "diamonds": 2,  # 1 bean = 2 diamonds
        "usd": 0.05     # 1 bean = $0.05
    },
    "diamonds": {
        "beans": 0.5,   # 1 diamond = 0.5 beans
        "usd": 0.025    # 1 diamond = $0.025
    },
    "usd": {
        "beans": 20,    # $1 = 20 beans
        "diamonds": 40  # $1 = 40 diamonds
    }
}

tiers = [
    {"name": "Rookie", "beans": 0, "hours": 0},
    {"name": "Explorer", "beans": 5000, "hours": 60},
    {"name": "Rising Star", "beans": 15000, "hours": 80},
    {"name": "Talent", "beans": 30000, "hours": 100},
    {"name": "Professional", "beans": 60000, "hours": 120},
    {"name": "Elite", "beans": 100000, "hours": 150},
    {"name": "Champion", "beans": 200000, "hours": 180}
]

events = [
    {"name": "Summer Bash", "type": "Contest", "entry_fee": 500, "participants": "12/20", "duration": "5 days", "prize": "10,000 beans"},
    {"name": "Talent Showcase", "type": "Exhibition", "entry_fee": 0, "participants": "8/15", "duration": "3 days", "prize": "Promotion opportunity"},
    {"name": "Team Challenge", "type": "Competition", "entry_fee": 1000, "participants": "24/30", "duration": "7 days", "prize": "25,000 beans + sponsorship"}
]

growth_strategies = {
    "default": "Focus on consistency, engaging with viewers, collaborating with other streamers, and cross-platform promotion.",
    "instagram": "Post daily stories, weekly carousel posts, and use relevant hashtags. Promote your Bigo Live schedule.",
    "tiktok": "Create 3-5 short clips daily from your streams. Use trending sounds and participate in challenges.",
    "youtube": "Upload weekly highlight videos and monthly best-of compilations. Optimize titles and thumbnails.",
    "twitter": "Tweet updates before going live, share screenshots, and engage with your community frequently."
}

# Tool function definitions
def convert_currency(type: str, amount: float) -> str:
    """Convert between diamonds, beans, and USD"""
    if type not in conversion_rates:
        return json.dumps({"error": "Valid types are: beans, diamonds, usd"})
    
    if amount <= 0:
        return json.dumps({"error": "Amount must be a positive number"})
    
    diamond_value = amount if type == 'diamonds' else amount * conversion_rates[type]['diamonds']
    beans_value = amount if type == 'beans' else amount * conversion_rates[type]['beans']
    usd_value = amount if type == 'usd' else amount * conversion_rates[type]['usd']
    
    return json.dumps({
        "diamond_value": diamond_value,
        "beans_value": beans_value,
        "usd_value": usd_value
    })

def track_progress(beans: int, hours: int) -> str:
    """Track progress and get next tier information"""
    if beans < 0 or hours < 0:
        return json.dumps({"error": "Beans and hours must be positive numbers"})
    
    current_tier = tiers[0]
    next_tier = tiers[1]
    
    for i in range(len(tiers) - 1, -1, -1):
        if beans >= tiers[i]["beans"] and hours >= tiers[i]["hours"]:
            current_tier = tiers[i]
            next_tier = tiers[i+1] if i < len(tiers) - 1 else None
            break
    
    if not next_tier:
        return json.dumps({
            "current_tier": current_tier["name"],
            "current_beans": beans,
            "current_hours": hours,
            "status": "Congratulations! You've reached the highest tier!"
        })
    
    beans_needed = next_tier["beans"] - beans
    hours_needed = next_tier["hours"] - hours
    
    return json.dumps({
        "current_tier": current_tier["name"],
        "current_beans": beans,
        "current_hours": hours,
        "next_tier": next_tier["name"],
        "beans_needed": beans_needed,
        "hours_needed": max(0, hours_needed)
    })

def get_events() -> str:
    """Get current events from Bigo Live"""
    return json.dumps({"events": events})

def get_growth_strategy(platform: Optional[str] = None) -> str:
    """Get growth strategy for a specific platform or general guide"""
    if not platform or platform not in growth_strategies:
        return json.dumps({
            "strategy": growth_strategies["default"],
            "available_platforms": list(growth_strategies.keys())
        })
    
    return json.dumps({"platform": platform, "strategy": growth_strategies[platform]})

def get_sponsorship_info(followers: int) -> str:
    """Get sponsorship tier information based on follower count"""
    if followers < 0:
        return json.dumps({"error": "Followers must be a positive number"})
    
    if followers < 5000:
        tier = "Micro-Influencer"
        benefits = "Product gifts, small commissions"
    elif followers < 20000:
        tier = "Rising Influencer"
        benefits = "Product gifts, paid promotions (up to $200)"
    elif followers < 50000:
        tier = "Mid-Tier Influencer"
        benefits = "Paid promotions ($200-$500), affiliate opportunities"
    elif followers < 100000:
        tier = "Established Influencer"
        benefits = "Paid promotions ($500-$1000), brand partnerships"
    else:
        tier = "Top Influencer"
        benefits = "Premium brand deals ($1000+), exclusive partnerships"
    
    return json.dumps({
        "followers": followers,
        "tier": tier,
        "benefits": benefits
    })

def get_wishlist_guide() -> str:
    """Get Amazon wishlist setup guide"""
    guide_steps = [
        "Create an Amazon account if you don't have one",
        "Go to Account & Lists > Create a List",
        "Click 'Create a List'",
        "Name your wishlist 'Stream Wishlist' or similar",
        "Set privacy to 'Public'",
        "Add items that would enhance your stream",
        "Share the link with your viewers"
    ]
    
    tips = [
        "Include a mix of price points",
        "Add stream equipment, gaming gear, and fun items",
        "Thank viewers publicly when they purchase items",
        "Update the list regularly"
    ]
    
    return json.dumps({
        "steps": guide_steps,
        "tips": tips
    })

def get_cross_promotion() -> str:
    """Get cross-platform promotion strategy"""
    strategies = {
        "brand_consistency": "Use the same username, profile picture, and bio across platforms",
        "platform_specific": {
            "tiktok": "Short clips with trending sounds",
            "instagram": "Stories announcing streams, highlights",
            "youtube": "Longer highlights, tutorials, vlogs",
            "twitter": "Stream announcements, interact with community"
        },
        "cross_linking": "Always include links to your other platforms in your bio",
        "schedule": "Post your streaming schedule on all platforms"
    }
    
    return json.dumps(strategies)

def get_strategy(beans: int, hours: int) -> str:
    """Get trading strategy suggestions"""
    if beans < 0 or hours < 0:
        return json.dumps({"error": "Beans and hours must be positive numbers"})
    
    hourly_rate = beans / max(1, hours)  # Avoid division by zero
    target_hourly_rate = hourly_rate * 1.2  # 20% improvement target
    
    if hourly_rate < 100:
        recommended_hours = "4-5 hours daily"
        recommended_activities = "Focus on engagement, host multi-guest rooms, participate in events"
    elif hourly_rate < 300:
        recommended_hours = "3-4 hours daily"
        recommended_activities = "Host themed streams, collaborate with other streamers, run contests"
    elif hourly_rate < 600:
        recommended_hours = "2-3 hours daily"
        recommended_activities = "Focus on peak hours, partner with agencies, create exclusive content"
    else:
        recommended_hours = "2 hours at peak times"
        recommended_activities = "Premium content, exclusive collaborations, develop off-platform presence"
    
    return json.dumps({
        "current_beans": beans,
        "current_hours": hours,
        "current_hourly_rate": round(hourly_rate),
        "target_hourly_rate": round(target_hourly_rate),
        "recommended_hours": recommended_hours,
        "recommended_activities": recommended_activities,
        "monthly_targets": {
            "beans": round(target_hourly_rate * 30 * 3),
            "hours": 90,
            "event_beans": round(beans * 0.1)
        }
    })

def get_event_info(event_name: Optional[str] = None) -> str:
    """Get information about a specific event or list all active events"""
    if not event_name:
        return json.dumps({"events": [event["name"] for event in events]})
    
    event = next((e for e in events if e["name"].lower() == event_name.lower()), None)
    if not event:
        return json.dumps({"error": f'Event "{event_name}" not found'})
    
    return json.dumps(event)

def join_event(event_name: str) -> str:
    """Join an event by its name"""
    if not event_name:
        return json.dumps({"error": "Event name is required"})
    
    event = next((e for e in events if e["name"].lower() == event_name.lower()), None)
    if not event:
        return json.dumps({"error": f'Event "{event_name}" not found'})
    
    return json.dumps({
        "status": "success",
        "message": f'You\'ve successfully joined the "{event["name"]}" event!',
        "event_details": event
    })

def get_loan_info() -> str:
    """Get information about the loan system"""
    loan_tiers = [
        {"name": "Starter", "limit": 5000, "interest": "10%", "term": "30 days"},
        {"name": "Growth", "limit": 20000, "interest": "8%", "term": "60 days"},
        {"name": "Professional", "limit": 50000, "interest": "6%", "term": "90 days"},
        {"name": "Elite", "limit": 100000, "interest": "5%", "term": "120 days"}
    ]
    
    requirements = [
        "Active on Bigo Live for at least 30 days",
        "Minimum credit score (use !credit_score to check)",
        "Regular streaming schedule"
    ]
    
    return json.dumps({
        "loan_tiers": loan_tiers,
        "requirements": requirements
    })

def get_credit_score() -> str:
    """Simulate checking a user's credit score"""
    import random
    score = random.randint(300, 850)
    
    if score < 500:
        rating = "Poor"
        eligible = "Starter loans with guarantor"
    elif score < 650:
        rating = "Fair"
        eligible = "Starter loans"
    elif score < 750:
        rating = "Good"
        eligible = "Starter and Growth loans"
    elif score < 800:
        rating = "Very Good"
        eligible = "All loan tiers except Elite"
    else:
        rating = "Excellent"
        eligible = "All loan tiers"
    
    improvements = [
        "Stream consistently",
        "Participate in community events",
        "Repay loans on time",
        "Increase your bean earnings",
        "Maintain active status"
    ]
    
    return json.dumps({
        "score": score,
        "rating": rating,
        "eligible": eligible,
        "improvements": improvements
    })

# Pydantic model for command parsing
class CommandParameters(BaseModel):
    command: str = Field(..., description="The command name without the ! prefix")
    args: Dict[str, Any] = Field(default_factory=dict, description="Command arguments as key-value pairs")

# Define tools for Groq API
tools = [
    {
        "type": "function",
        "function": {
            "name": "parse_command",
            "description": "Parse a Discord bot command and extract command name and arguments",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command name without the ! prefix (e.g., 'convert', 'track')"
                    },
                    "args": {
                        "type": "object",
                        "description": "Command arguments as key-value pairs",
                        "additionalProperties": {
                            "type": "string"
                        }
                    }
                },
                "required": ["command"]
            }
        }
    }
]

# Map command names to their functions
command_functions = {
    "convert": convert_currency,
    "track": track_progress,
    "events": get_events,
    "growth": get_growth_strategy,
    "sponsorship": get_sponsorship_info,
    "wishlist": get_wishlist_guide,
    "cross_promote": get_cross_promotion,
    "strategy": get_strategy,
    "event_info": get_event_info,
    "join_event": join_event,
    "loan_info": get_loan_info,
    "credit_score": get_credit_score
}

# Function to process commands with conversation memory
def process_command(user_input: str, conversation_history: str = "") -> str:
    """Process a user input and intelligently decide which command to run or respond conversationally, using conversation history"""
    system_message = """You are Bean-Genie, a Discord bot for Bigo Live streamers.
    You can understand natural language input and decide which command to run if any.
    If the input is a command, extract the command name and arguments.
    If the input is conversational, respond appropriately without requiring a command prefix.
    Use the conversation history to maintain context.
    """
    
    # Combine conversation history and current user input
    combined_input = conversation_history + "\nUser: " + user_input
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": combined_input}
    ]
    
    try:
        # Use the Groq client to get a response that decides what to do
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Try to parse content as JSON command call
        try:
            parsed = json.loads(content)
            command = parsed.get("command", "").lower()
            args = parsed.get("args", {})
            if command in command_functions:
                return command_functions[command](**args)
            else:
                # If command unknown, return content as is
                return content
        except Exception:
            # If not JSON, return content as conversational response
            return content
        
    except Exception as e:
        return json.dumps({"error": f"Error processing input: {str(e)}"})

# Example usage
def format_response(response):
    """Format the response for display"""
    try:
        data = json.loads(response)
    except Exception:
        return response
    
    if "error" in data:
        return f"❌ Error: {data['error']}"
    
    formatted = []
    for key, value in data.items():
        if isinstance(value, dict):
            formatted.append(f"**{key.replace('_', ' ').title()}:**")
            for k, v in value.items():
                formatted.append(f"  - {k.replace('_', ' ').title()}: {v}")
        elif isinstance(value, list):
            formatted.append(f"**{key.replace('_', ' ').title()}:**")
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        formatted.append(f"  - {k.replace('_', ' ').title()}: {v}")
                else:
                    formatted.append(f"  - {item}")
        else:
            formatted.append(f"**{key.replace('_', ' ').title()}:** {value}")
    return "\n".join(formatted)

# CLI application
def run_cli():
    print("Bean-Genie Discord Bot (CLI Version)")
    print("Type a command (e.g., !convert beans 1000) or 'exit' to quit.")
    print("-" * 50)
    
    while True:
        user_input = input("\nEnter command: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = process_command(user_input)
        print("\nResponse:")
        print(format_response(response))
        print("-" * 50)

if __name__ == "__main__":
    run_cli()
