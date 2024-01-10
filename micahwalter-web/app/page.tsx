import Image from 'next/image'
import christmasPic from '../public/images/IMG_4128.jpg'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl">Hello</h1>

      <Image
        src={christmasPic}
        alt="Christmas at the Walter home."
      />
      
    </main>
  )
}
