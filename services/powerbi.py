class PowerBiService:
    @staticmethod
    def get_dashboard_config():
        """
        Returns parameters required for Power BI Embedded.
        In a production system, this would call Azure Active Directory to get an access token
        and retrieve the Embed URL for the report.
        """
        return {
            "enabled": False, # Switch to True when real client ID / workspace ID are configured
            "report_id": "00000000-0000-0000-0000-000000000000",
            "workspace_id": "00000000-0000-0000-0000-000000000000",
            "embed_url": "https://app.powerbi.com/reportEmbed?reportId=mock_report_id&groupId=mock_group_id",
            "access_token": "mock_powerbi_embed_token",
            "placeholder_message": "Power BI Embedded service is ready. Configure credentials in Azure AD to see the live dashboard."
        }
