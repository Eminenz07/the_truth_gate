"""
Brevo (Sendinblue) Email Service Integration

This module provides helper functions for sending transactional emails (follow-ups)
and bulk emails (newsletters) via the Brevo API.

Configuration:
- Set BREVO_API_KEY in your environment variables
- Verify your sender email in Brevo dashboard
"""

import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Check if Brevo is configured
BREVO_CONFIGURED = bool(getattr(settings, 'BREVO_API_KEY', None))

if BREVO_CONFIGURED:
    import sib_api_v3_sdk
    from sib_api_v3_sdk.rest import ApiException
    
    # Configure API client
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY


def get_default_followup_template(name: str = "Friend") -> dict:
    """
    Returns the default follow-up email template.
    """
    return {
        'subject': 'Following Up on Your Prayer Request',
        'message': f"""Dear {name},

Thank you for sharing your prayer request with us. We have been lifting you up in prayer, and wanted to personally reach out to see how you are doing.

[Your personal message here]

May God's peace and presence be with you during this time. Please don't hesitate to reach out if you need anything.

In Christ,
The Truth Gate Ministry
"""
    }


def send_followup_email(to_email: str, to_name: str, subject: str, html_content: str, sender_name: str = "The Truth Gate", sender_email: str = None) -> dict:
    """
    Send a transactional follow-up email to a single recipient.
    
    Args:
        to_email: Recipient email address
        to_name: Recipient name
        subject: Email subject line
        html_content: HTML body of the email
        sender_name: Name to show as sender
        sender_email: Email to send from (must be verified in Brevo)
    
    Returns:
        dict with 'success' (bool) and 'message' or 'error'
    """
    if not BREVO_CONFIGURED:
        logger.warning("Brevo API key not configured. Email not sent.")
        return {
            'success': False,
            'error': 'Email service not configured. Please add BREVO_API_KEY to environment variables.'
        }
    
    # Use configured sender email or fall back
    if not sender_email:
        sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@thetruthgate.org')
    
    try:
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        
        # Build the email
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email, "name": to_name}],
            sender={"name": sender_name, "email": sender_email},
            subject=subject,
            html_content=html_content.replace('\n', '<br>')
        )
        
        # Send it
        response = api_instance.send_transac_email(send_smtp_email)
        logger.info(f"Follow-up email sent to {to_email}. Message ID: {response.message_id}")
        
        return {
            'success': True,
            'message': f'Email sent successfully to {to_email}',
            'message_id': response.message_id
        }
        
    except ApiException as e:
        logger.error(f"Brevo API error sending follow-up: {e}")
        return {
            'success': False,
            'error': f'Failed to send email: {str(e)}'
        }
    except Exception as e:
        logger.error(f"Unexpected error sending follow-up email: {e}")
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def send_newsletter(subject: str, html_content: str, subscribers: list, sender_name: str = "The Truth Gate", sender_email: str = None) -> dict:
    """
    Send a newsletter to multiple subscribers.
    
    Args:
        subject: Newsletter subject line
        html_content: HTML body of the newsletter
        subscribers: List of dicts with 'email' and optional 'name'
        sender_name: Name to show as sender
        sender_email: Email to send from (must be verified in Brevo)
    
    Returns:
        dict with 'success' (bool), 'sent_count', and 'errors'
    """
    if not BREVO_CONFIGURED:
        logger.warning("Brevo API key not configured. Newsletter not sent.")
        return {
            'success': False,
            'error': 'Email service not configured. Please add BREVO_API_KEY to environment variables.',
            'sent_count': 0
        }
    
    if not subscribers:
        return {
            'success': False,
            'error': 'No subscribers to send to.',
            'sent_count': 0
        }
    
    # Use configured sender email or fall back
    if not sender_email:
        sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@thetruthgate.org')
    
    try:
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        
        # Build recipient list
        to_list = []
        for sub in subscribers:
            to_list.append({
                "email": sub.get('email'),
                "name": sub.get('name', '')
            })
        
        # Note: For large lists, Brevo recommends using Campaigns API
        # This approach works for smaller lists (< 99 recipients per call)
        # For larger lists, we batch the sends
        
        sent_count = 0
        errors = []
        batch_size = 50  # Brevo allows up to 99 per transactional email
        
        for i in range(0, len(to_list), batch_size):
            batch = to_list[i:i + batch_size]
            
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=batch,
                sender={"name": sender_name, "email": sender_email},
                subject=subject,
                html_content=html_content.replace('\n', '<br>')
            )
            
            try:
                response = api_instance.send_transac_email(send_smtp_email)
                sent_count += len(batch)
                logger.info(f"Newsletter batch sent: {len(batch)} recipients. Message ID: {response.message_id}")
            except ApiException as e:
                errors.append(f"Batch {i//batch_size + 1} failed: {str(e)}")
                logger.error(f"Newsletter batch failed: {e}")
        
        return {
            'success': sent_count > 0,
            'sent_count': sent_count,
            'total_subscribers': len(subscribers),
            'errors': errors if errors else None
        }
        
    except Exception as e:
        logger.error(f"Unexpected error sending newsletter: {e}")
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'sent_count': 0
        }
