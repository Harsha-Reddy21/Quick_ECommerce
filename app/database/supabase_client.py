from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

class SupabaseService:
    """Service class for Supabase operations"""
    
    @staticmethod
    def get_client() -> Client:
        """Get the Supabase client instance"""
        return supabase
    
    # User operations
    @staticmethod
    def get_user_by_email(email: str):
        """Get user by email"""
        response = supabase.table("users").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """Get user by ID"""
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_user(user_data: dict):
        """Create a new user"""
        response = supabase.table("users").insert(user_data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_user(user_id: int, user_data: dict):
        """Update user data"""
        response = supabase.table("users").update(user_data).eq("id", user_id).execute()
        return response.data[0] if response.data else None
    
    # Medicine operations
    @staticmethod
    def get_all_medicines(limit: int = 100, offset: int = 0):
        """Get all medicines with pagination"""
        response = supabase.table("medicines").select("*").range(offset, offset + limit - 1).execute()
        return response.data
    
    @staticmethod
    def get_medicine_by_id(medicine_id: int):
        """Get medicine by ID"""
        response = supabase.table("medicines").select("*").eq("id", medicine_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_medicine(medicine_data: dict):
        """Create a new medicine"""
        response = supabase.table("medicines").insert(medicine_data).execute()
        return response.data[0] if response.data else None
    
    # Category operations
    @staticmethod
    def get_all_categories():
        """Get all categories"""
        response = supabase.table("categories").select("*").execute()
        return response.data
    
    @staticmethod
    def get_medicines_by_category(category_id: int, limit: int = 100, offset: int = 0):
        """Get medicines by category"""
        response = supabase.table("medicines").select("*").eq("category_id", category_id).range(offset, offset + limit - 1).execute()
        return response.data
    
    # Cart operations
    @staticmethod
    def get_cart_by_user_id(user_id: int):
        """Get cart by user ID"""
        response = supabase.table("carts").select("*").eq("user_id", user_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_cart_items(cart_id: int):
        """Get cart items by cart ID"""
        response = supabase.table("cart_items").select("*").eq("cart_id", cart_id).execute()
        return response.data
    
    @staticmethod
    def add_cart_item(cart_item_data: dict):
        """Add item to cart"""
        response = supabase.table("cart_items").insert(cart_item_data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_cart_item(cart_item_id: int, cart_item_data: dict):
        """Update cart item"""
        response = supabase.table("cart_items").update(cart_item_data).eq("id", cart_item_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_cart_item(cart_item_id: int):
        """Delete cart item"""
        response = supabase.table("cart_items").delete().eq("id", cart_item_id).execute()
        return response.data[0] if response.data else None
    
    # Order operations
    @staticmethod
    def create_order(order_data: dict):
        """Create a new order"""
        response = supabase.table("orders").insert(order_data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def add_order_item(order_item_data: dict):
        """Add item to order"""
        response = supabase.table("order_items").insert(order_item_data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_orders_by_user_id(user_id: int):
        """Get orders by user ID"""
        response = supabase.table("orders").select("*").eq("user_id", user_id).execute()
        return response.data
    
    @staticmethod
    def get_order_by_id(order_id: int):
        """Get order by ID"""
        response = supabase.table("orders").select("*").eq("id", order_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_order_items(order_id: int):
        """Get order items by order ID"""
        response = supabase.table("order_items").select("*").eq("order_id", order_id).execute()
        return response.data
    
    @staticmethod
    def update_order_status(order_id: int, status: str):
        """Update order status"""
        response = supabase.table("orders").update({"status": status}).eq("id", order_id).execute()
        return response.data[0] if response.data else None
    
    # Prescription operations
    @staticmethod
    def get_prescriptions_by_user_id(user_id: int):
        """Get prescriptions by user ID"""
        response = supabase.table("prescriptions").select("*").eq("user_id", user_id).execute()
        return response.data
    
    @staticmethod
    def create_prescription(prescription_data: dict):
        """Create a new prescription"""
        response = supabase.table("prescriptions").insert(prescription_data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def verify_prescription(prescription_id: int, verified_by: int):
        """Verify a prescription"""
        response = supabase.table("prescriptions").update({
            "is_verified": True,
            "verified_by": verified_by
        }).eq("id", prescription_id).execute()
        return response.data[0] if response.data else None

# Create a singleton instance
db_service = SupabaseService() 