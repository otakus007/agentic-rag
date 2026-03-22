import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FileUploadZone from '../FileUploadZone.vue'

describe('FileUploadZone', () => {
  it('renders drop zone with instructions', () => {
    const wrapper = mount(FileUploadZone)
    expect(wrapper.text()).toContain('Browse files')
    expect(wrapper.text()).toContain('drag and drop PDF files')
    expect(wrapper.text()).toContain('PDF files only')
  })

  it('has a hidden file input with pdf accept', () => {
    const wrapper = mount(FileUploadZone)
    const input = wrapper.find('input[type="file"]')
    expect(input.exists()).toBe(true)
    expect(input.attributes('accept')).toBe('.pdf')
    expect(input.attributes('multiple')).toBeDefined()
  })

  it('has an agent ID input', () => {
    const wrapper = mount(FileUploadZone)
    const input = wrapper.find('input[type="text"]')
    expect(input.exists()).toBe(true)
    expect(input.attributes('placeholder')).toContain('Agent ID')
  })
})
