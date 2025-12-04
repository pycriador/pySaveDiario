#!/usr/bin/env python3
"""
Initialize default social network configurations
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import SocialNetworkConfig


def init_social_networks():
    """Initialize default social network configurations"""
    
    app = create_app()
    
    with app.app_context():
        networks = [
            {
                'network': 'instagram',
                'prefix_text': '',
                'suffix_text': '#ofertas #descontos #promoção',
                'active': True
            },
            {
                'network': 'facebook',
                'prefix_text': '🔥 OFERTA IMPERDÍVEL!\n\n',
                'suffix_text': '\n\n👍 Curta nossa página para não perder promoções!',
                'active': True
            },
            {
                'network': 'whatsapp',
                'prefix_text': '💰 *PROMOÇÃO*\n\n',
                'suffix_text': '\n\n_Compartilhe com quem precisa!_',
                'active': True
            },
            {
                'network': 'telegram',
                'prefix_text': '📢 NOVA OFERTA!\n\n',
                'suffix_text': '\n\n🔔 Ative as notificações do canal!',
                'active': True
            }
        ]
        
        for net_data in networks:
            existing = SocialNetworkConfig.query.filter_by(network=net_data['network']).first()
            if not existing:
                config = SocialNetworkConfig(**net_data)
                db.session.add(config)
                print(f"✓ Created config for {net_data['network']}")
            else:
                print(f"⊘ Config for {net_data['network']} already exists")
        
        db.session.commit()
        print("\n✅ Social network configurations initialized successfully!")


if __name__ == '__main__':
    init_social_networks()

