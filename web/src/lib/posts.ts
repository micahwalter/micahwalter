import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import html from 'remark-html'

const postsDirectory = path.join(process.cwd(), 'src/content/posts')

export interface Post {
  slug: string
  title: string
  date: string
  content: string
  excerpt?: string
}

export async function getPost(slug: string): Promise<Post | null> {
  try {
    const fullPath = path.join(postsDirectory, `${slug}.md`)
    const fileContents = fs.readFileSync(fullPath, 'utf8')
    const { data, content } = matter(fileContents)
    
    const processedContent = await remark()
      .use(html)
      .process(content)
    
    return {
      slug,
      title: data.title,
      date: data.date,
      content: processedContent.toString(),
      excerpt: data.excerpt
    }
  } catch (error) {
    // Log the error in development
    if (process.env.NODE_ENV === 'development') {
      console.error(`Error loading post ${slug}:`, error)
    }
    return null
  }
}

export function getAllPosts(): Post[] {
  const fileNames = fs.readdirSync(postsDirectory)
  const posts = fileNames.map(fileName => {
    const slug = fileName.replace(/\.md$/, '')
    const fullPath = path.join(postsDirectory, fileName)
    const fileContents = fs.readFileSync(fullPath, 'utf8')
    const { data } = matter(fileContents)
    
    return {
      slug,
      title: data.title,
      date: data.date,
      content: '',
      excerpt: data.excerpt
    }
  })
  
  return posts.sort((a, b) => (a.date < b.date ? 1 : -1))
}