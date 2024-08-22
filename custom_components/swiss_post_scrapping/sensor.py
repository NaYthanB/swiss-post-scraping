from homeassistant.helpers.entity import Entity

DOMAIN = "swiss_post_scrapping"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Swiss Post Scrapping sensors from a config entry."""
    
    # Créer une instance du capteur et l'ajouter
    async_add_entities([SwissPostTrackingSensor(hass)])

class SwissPostTrackingSensor(Entity):
    """Sensor to display the tracking numbers from Swiss Post."""

    def __init__(self, hass, name="Swiss Post Tracking Numbers"):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        tracking_numbers = self._hass.data.get(DOMAIN, {}).get("tracking_numbers", [])
        if tracking_numbers:
            return ', '.join(tracking_numbers)
        return "No data"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        tracking_numbers = self._hass.data.get(DOMAIN, {}).get("tracking_numbers", [])
        if tracking_numbers:
            self._state = ', '.join(tracking_numbers)
        else:
            self._state = "No data"