import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import SourceCard from '../SourceCard.vue'

describe('SourceCard', () => {
  const mockSource = {
    content: 'The leave policy allows 20 days annually.',
    page_number: 5,
    block_type: 'paragraph',
  }

  it('renders content, page number, and block type', () => {
    const wrapper = mount(SourceCard, {
      props: { source: mockSource, index: 1, active: false },
    })
    expect(wrapper.text()).toContain('The leave policy allows 20 days annually.')
    expect(wrapper.text()).toContain('p. 5')
    expect(wrapper.text()).toContain('paragraph')
    expect(wrapper.text()).toContain('1')
  })

  it('highlights when active', () => {
    const wrapper = mount(SourceCard, {
      props: { source: mockSource, index: 1, active: true },
    })
    expect(wrapper.html()).toContain('bg-cta/10')
    expect(wrapper.html()).toContain('border-cta/40')
  })

  it('uses default styling when not active', () => {
    const wrapper = mount(SourceCard, {
      props: { source: mockSource, index: 1, active: false },
    })
    expect(wrapper.html()).toContain('bg-surface-light')
  })
})
