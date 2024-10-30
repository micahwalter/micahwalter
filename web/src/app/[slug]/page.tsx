import { getPost, getAllPosts } from '@/lib/posts'
import { notFound } from 'next/navigation'

interface PageProps {
  params: Promise<{
    slug: string
  }>
}

export async function generateStaticParams() {
  const posts = getAllPosts()
  return posts.map((post) => ({
    slug: post.slug,
  }))
}

export default async function BlogPost({ params }: PageProps) {
  const resolvedParams = await params
  const post = await getPost(resolvedParams.slug)
  
  if (!post) {
    notFound()
  }

  return (
    <article className="max-w-2xl mx-auto px-6 py-12">
      <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
      <time className="text-gray-600 mb-8 block">
        {new Date(post.date).toLocaleDateString()}
      </time>
      <div 
        className="prose prose-lg"
        dangerouslySetInnerHTML={{ __html: post.content }} 
      />
    </article>
  )
}