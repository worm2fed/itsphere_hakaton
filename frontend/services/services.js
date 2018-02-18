import vue from 'vue'
import resource from 'vue-resource'

vue.use(resource)

export const http = vue.http

export const Page = vue.resource('/api/pages{/permlink}/')
export const Tag = vue.resource('/api/tags{/id}/')
export const Comment = vue.resource('/api/comments{/id}/')
//export const Avatar = vue.resource('/api/users/{/id}/set_avatar/')

export const MasterTag = vue.resource('/api/master-tags{/id}/', {}, {
	'tree': {
		method: 'GET', url: '/api/master-tags/tree/'
	},
	'ancestors': {
		method: 'GET', url: '/api/master-tags{/id}/ancestors/'
	}
})

export const Avatar = vue.resource('/api/users/{/id}/', {}, {
  'post': {
    method: 'POST', url: '/api/users{/id}/set_avatar/'
  }
})

export const User = vue.resource('/api/users{/id}/', {}, {
	'current': { method: 'GET', url: '/api/users/current/' },
	'signUp': { method: 'POST', url: '/sign-up/' },
})
