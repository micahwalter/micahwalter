import Link from 'next/link'
import { getAllPosts } from '@/lib/posts'

export default function Home() {
  const posts = getAllPosts()

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <h1 className="text-4xl font-bold mb-8">Blog Posts</h1>
      <div className="space-y-8">
        {posts.map((post) => (
          <article key={post.slug}>
            <Link href={`/${post.slug}`}>
              <h2 className="text-2xl font-semibold hover:text-blue-600">
                {post.title}
              </h2>
            </Link>
            <time className="text-gray-600 block mt-2">
              {new Date(post.date).toLocaleDateString()}
            </time>
            {post.excerpt && (
              <p className="mt-3 text-gray-600">{post.excerpt}</p>
            )}
          </article>
        ))}
      </div>
    </div>
  )
}