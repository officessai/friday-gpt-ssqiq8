import { CapabilitiesList } from './components/CapabilitiesList'
import { HeroSection } from './components/HeroSection'
import { StackList } from './components/StackList'

function App() {
  return (
    <main className="layout">
      <HeroSection />
      <CapabilitiesList />
      <StackList />
    </main>
  )
}

export default App
