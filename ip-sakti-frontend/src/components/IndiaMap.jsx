import React, { useState } from 'react'
import { MapContainer, TileLayer, GeoJSON, Marker, Popup, useMap } from 'react-leaflet'
import { useTranslation } from 'react-i18next'
import 'leaflet/dist/leaflet.css'

const INDIA_CENTER = [20.5937, 78.9629]

function FitBounds({ bounds }) {
  const map = useMap()
  if (bounds) {
    map.fitBounds(bounds)
  }
  return null
}

export default function IndiaMap({ data, onStateClick, selectedState }) {
  const { t } = useTranslation()
  const [hoveredState, setHoveredState] = useState(null)

  const getColor = (count, max) => {
    const ratio = count / (max || 1)
    if (ratio > 0.7) return '#dc2626'
    if (ratio > 0.5) return '#f97316'
    if (ratio > 0.3) return '#fbbf24'
    if (ratio > 0.1) return '#84cc16'
    return '#22c55e'
  }

  const maxValue = Math.max(...data.map(d => d.gi_tags + d.patents + d.formulations))

  const onEachFeature = (feature, layer) => {
    layer.on({
      click: () => {
        const stateData = data.find(d => d.state_name === feature.properties.NAME_1)
        if (stateData && onStateClick) {
          onStateClick({
            ...stateData,
            name: feature.properties.NAME_1,
          })
        }
      },
      mouseover: () => setHoveredState(feature.properties.NAME_1),
      mouseout: () => setHoveredState(null),
    })
  }

  const style = (feature) => {
    const stateData = data.find(d => d.state_name === feature.properties.NAME_1)
    const count = stateData ? stateData.gi_tags + stateData.patents + stateData.formulations : 0
    return {
      fillColor: getColor(count, maxValue),
      weight: hoveredState === feature.properties.NAME_1 || selectedState?.name === feature.properties.NAME_1 ? 3 : 1,
      opacity: 1,
      color: 'white',
      dashArray: '0',
      fillOpacity: 0.7,
    }
  }

  return (
    <MapContainer
      center={INDIA_CENTER}
      zoom={5}
      style={{ height: '500px', width: '100%', borderRadius: '0.75rem' }}
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {data.map((stateData) => {
        if (!stateData.latitude || !stateData.longitude) return null
        return (
          <Marker key={stateData.state_id} position={[stateData.latitude, stateData.longitude]}>
            <Popup>
              <div className="p-2">
                <h3 className="font-semibold">{stateData.state_name}</h3>
                <p className="text-sm">GI Tags: {stateData.gi_tags}</p>
                <p className="text-sm">Formulations: {stateData.formulations}</p>
              </div>
            </Popup>
          </Marker>
        )
      })}
    </MapContainer>
  )
}
